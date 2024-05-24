#!/usr/bin/env python3
"""Module to test the Authentication route
"""
from config import TestConfig
from datetime import datetime, timedelta
from db import db, redis_client as rc
from flask_jwt_extended import create_access_token
from routes.auth import store_token
from main import create_app
import unittest
from bson import ObjectId
import json
import random


class TestGetFeedPosts(unittest.TestCase):
    """ Tests for 'GET /feed/get_posts' route """

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests
        """

        # Create app
        cls.app = create_app(TestConfig)

        # Create client
        cls.client = cls.app.test_client()

        # Create dummy user
        infos = {
            'username': 'albushog99',
            'email': 'lumos@poud.mgc',
            'password': 'gumbledore',
            'longest_streak': 0
        }
        user_id = str(db.insert_user(infos))

        # Create another dummy user
        infos = {
            'username': 'tomdemort67',
            'email': 'riddle@poud.mgc',
            'password': 'serpentard',
            'longest_streak': 0
        }
        another_user_id = str(db.insert_user(infos))

        # Create JWT Access Token
        with cls.app.app_context():
            cls.access_token = create_access_token(
                identity=user_id
            )

        # Store JWT Access Token
        store_token(
            user_id,
            cls.access_token,
            cls.app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )

        # Create dummy posts
        cls.public_posts = []

        for i in range(1, 87):

            title = f'Title {i}'
            content = f'This is post {i}'
            is_public = True if i % 2 == 0 else False
            datePosted = datetime.utcnow() + timedelta(days=i)

            post = {
                'user_id': random.choice([user_id, another_user_id]),
                'title': title,
                'content': content,
                'is_public': is_public,
                'datePosted': datePosted
            }

            if i % 2 == 0:
                cls.public_posts.append(post.copy())

            db.insert_post(post)

        # Sort posts
        cls.public_posts.sort(key=lambda x: x['datePosted'], reverse=True)

        # Stringify datePosted
        for p in cls.public_posts:
            p['datePosted'] = p['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db.clear_db()

    def test_get_feed_with_no_token(self):
        """Test getting feed's posts with no authentication
        """
        response = self.client.get('/feed/get_posts')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_feed_with_wrong_token(self):
        """Test getting feed's posts with wrong authentication
        """
        response = self.client.get('/feed/get_posts', headers={
            'Authorization': 'Bearer ' + self.access_token + 'k'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_number_of_public_posts(self):
        """Check number of public_posts
        """
        self.assertEqual(len(self.public_posts), 43)

    def test_get_feed_without_pagination(self):
        """Test getting feed's posts without pagination
        """
        response = self.client.get('/feed/get_posts', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self.public_posts))

        for recieved, expected in zip(data, self.public_posts):
            self.assertEqual(recieved, expected)


class TestLikeUnlike(unittest.TestCase):
    """ Tests for liking and unliking routes """

    def setUp(self):
        """ Runs once before every test """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        info = {
            'email': 'mohamed@example.com',
            'username': 'mohamed',
            'password': 'pass123',
            'longest_streak': 0
        }

        self.user_id = db.insert_user(info)

        self.dummy_user = ObjectId()
        self.post_info = {
            'user_id': self.dummy_user,
            'title': 'Post title',
            'content': 'Post content',
            'is_public': 'true',
            'likes': [],
            'number_of_likes': 0,
            'date_posted': datetime.utcnow()
        }
        self.post_id = db.insert_post(self.post_info)

        self.login_detail = {
            'email': 'mohamed@example.com',
            'password': 'pass123'
        }
        res = self.client.post('/login', json=self.login_detail)
        data = res.get_json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']

    def tearDown(self):
        """ Runs once after every test """
        db.clear_db()
        rc.flushall()

    def test_like_post(self):
        """" Test for liking posts for authed users """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
        }
        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, {'success': 'Post liked successfully.'})

        post = db.find_post({'_id': self.post_id, 'user_id': self.dummy_user})

        self.assertEqual(post['number_of_likes'], 1)
        self.assertIn(self.user_id, post['likes'])

    def test_like_post_twice(self):
        """" Test for liking posts that's already liked by the current user """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
        }
        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, {'success': 'Post liked successfully.'})

        post = db.find_post({'_id': self.post_id, 'user_id': self.dummy_user})

        self.assertEqual(post['number_of_likes'], 1)
        self.assertIn(self.user_id, post['likes'])

        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, {'error': 'User has already liked the post.'})

        post = db.find_post({'_id': self.post_id, 'user_id': self.dummy_user})

        self.assertEqual(post['number_of_likes'], 1)

    def test_like_none_existing_post(self):
        """" Test for liking posts that's does not exists. """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dummy_id = ObjectId()
        dump = {
            'post_id': str(dummy_id),
        }
        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data, {'error': 'Post not found.'})

        post = db.find_post({'_id': dummy_id, 'user_id': self.user_id})

        self.assertIsNone(post)

    def test_like_post_anonymous_user(self):
        """" Test for liking posts with an unathanticated user. """

        headers = {
            'Content-Type': 'application/json',
        }
        dump = {
            'post_id': str(self.post_id),
        }
        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_unlike_post(self):
        """" Test for unliking posts for authed users """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
        }

        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, {'success': 'Post liked successfully.'})

        post = db.find_post({'_id': self.post_id, 'user_id': self.dummy_user})

        self.assertEqual(post['number_of_likes'], 1)

        res = self.client.post(
            '/feed/unlike', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, {'success': 'Post unliked successfully.'})

        post = db.find_post({'_id': self.post_id, 'user_id': self.dummy_user})

        self.assertEqual(post['number_of_likes'], 0)
        self.assertNotIn(self.user_id, post['likes'])

    def test_unlike_post_twice(self):
        """" Test for unliking posts that's
        already unliked by the current user """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
        }
        res = self.client.post(
            '/feed/unlike', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            data, {'error': 'User can only unliked the post that he liked.'}
        )

        post = db.find_post({'_id': self.post_id, 'user_id': self.dummy_user})

        self.assertEqual(post['number_of_likes'], 0)
        self.assertNotIn(self.user_id, post['likes'])

    def test_unlike_none_existing_post(self):
        """" Test for unliking posts that's does not exists. """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dummy_id = ObjectId()
        dump = {
            'post_id': str(dummy_id),
        }
        res = self.client.post(
            '/feed/unlike', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data, {'error': 'Post not found.'})

        post = db.find_post({'_id': dummy_id, 'user_id': self.user_id})

        self.assertIsNone(post)

    def test_unlike_post_anonymous_user(self):
        """" Test for unliking posts with an unathanticated user. """

        headers = {
            'Content-Type': 'application/json',
        }
        dump = {
            'post_id': str(self.post_id),
        }
        res = self.client.post(
            '/feed/unlike', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})
