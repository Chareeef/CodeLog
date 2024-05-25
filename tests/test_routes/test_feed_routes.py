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

        for i in range(1, 84):

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

            if post['user_id'] == user_id:
                post['username'] = 'albushog99'
            else:
                post['username'] = 'tomdemort67'

            if i % 2 == 0:
                cls.public_posts.append(post.copy())

            db.insert_post(post)

        # Sort posts from the most to the less recent
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
        self.assertEqual(len(self.public_posts), 41)

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

    def test_get_feed_page_1(self):
        """Test getting first feed's page
        """
        response = self.client.get('/feed/get_posts?page=1', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 20)

        for recieved, expected in zip(data, self.public_posts[:20]):
            self.assertEqual(recieved, expected)

    def test_get_feed_page_2(self):
        """Test getting second feed's page
        """
        response = self.client.get('/feed/get_posts?page=2', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 20)

        for recieved, expected in zip(data, self.public_posts[20:40]):
            self.assertEqual(recieved, expected)

    def test_get_feed_page_3(self):
        """Test getting third feed's page
        """
        response = self.client.get('/feed/get_posts?page=3', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

        for recieved, expected in zip(data, self.public_posts[40:]):
            self.assertEqual(recieved, expected)

    def test_get_feed_page_4(self):
        """Test getting fourth feed's page
        """
        response = self.client.get('/feed/get_posts?page=4', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'info': 'page out of range'})

    def test_get_feed_invalid_page_0(self):
        """Test getting feed's with page=0
        """
        response = self.client.get('/feed/get_posts?page=0', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {'error': 'page number must be greater or equal to 1'}
        )

    def test_get_feed_negative_page(self):
        """Test getting feed's with page=-3
        """
        response = self.client.get('/feed/get_posts?page=-3', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data, {'error': 'page number must be greater or equal to 1'}
        )

    def test_get_feed_invalid_page_type(self):
        """Test getting feed's with page=page_1
        """
        response = self.client.get('/feed/get_posts?page=page_1', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'page argument must be an integer'})


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


class TestComments(unittest.TestCase):
    """ Testing comments for authenticated users """
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
            'comments': [],
            'number_of_comments': 0,
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

    def test_create_new_comment(self):
        """ Test for adding a new comment to a post document. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

    def test_find_comment(self):
        """ Test for findind a new comment. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        post = db.find_post({'_id': self.post_id})

        self.assertNotEqual(post['comments'], [])
        self.assertNotEqual(post['number_of_comments'], 0)

        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertIsNotNone(comment)
        self.assertEqual(data['data'], comment)

    def test_comment_anonymous(self):
        """ Test comment for unauthenticed users. """
        headers = {
            'Content-Type': 'application/json',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 'Missing Authorization Header')

    def test_update_comment(self):
        """ Test for updating a comment. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        post = db.find_post({'_id': self.post_id})

        self.assertNotEqual(post['comments'], [])
        self.assertNotEqual(post['number_of_comments'], 0)

        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertIsNotNone(comment)
        self.assertEqual(data['data'], comment)

        updated_comment = {
            'post_id': str(self.post_id),
            'comment_id': str(post['comments'][0]),
            'body': 'Updated comment'
        }
        res = self.client.put(
            '/feed/update_comment',
            headers=headers,
            data=json.dumps(updated_comment)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment updated successfully.')

        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertEqual(post['number_of_comments'], 1)
        self.assertEqual(data['data'], comment)

    def test_update_comment_with_no_body(self):
        """ Test for updating a comment with no body. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        post = db.find_post({'_id': self.post_id})

        self.assertNotEqual(post['comments'], [])
        self.assertNotEqual(post['number_of_comments'], 0)

        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertIsNotNone(comment)
        self.assertEqual(data['data'], comment)

        updated_comment = {
            'post_id': str(self.post_id),
            'comment_id': str(post['comments'][0]),
        }
        res = self.client.put(
            '/feed/update_comment',
            headers=headers,
            data=json.dumps(updated_comment)
        )
        data = res.get_json()
        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 'Missing body')
        self.assertEqual(comment['body'], dump['body'])

    def test_update_comment_with_no_postid(self):
        """ Test for updating a comment with no post_id. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        post = db.find_post({'_id': self.post_id})

        self.assertNotEqual(post['comments'], [])
        self.assertNotEqual(post['number_of_comments'], 0)

        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertIsNotNone(comment)
        self.assertEqual(data['data'], comment)

        updated_comment = {
            'comment_id': str(post['comments'][0]),
            'body': 'Updated comment'
        }
        res = self.client.put(
            '/feed/update_comment',
            headers=headers,
            data=json.dumps(updated_comment)
        )
        data = res.get_json()
        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 'Missing post_id')
        self.assertEqual(comment['body'], dump['body'])

    def test_update_comment_with_no_commentid(self):
        """ Test for updating a comment with no post_id. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        post = db.find_post({'_id': self.post_id})

        self.assertNotEqual(post['comments'], [])
        self.assertNotEqual(post['number_of_comments'], 0)

        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertIsNotNone(comment)
        self.assertEqual(data['data'], comment)

        updated_comment = {
            'post_id': str(self.post_id),
            'body': 'Updated comment'
        }
        res = self.client.put(
            '/feed/update_comment',
            headers=headers,
            data=json.dumps(updated_comment)
        )
        data = res.get_json()
        comment = db.find_comment(post['comments'][0], self.user_id)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 'Missing comment_id')
        self.assertEqual(comment['body'], dump['body'])

    def test_delete_comment(self):
        """ Test delete comment. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        comment_id = data['data']['_id']
        dump = {
            'post_id': str(self.post_id),
            'comment_id': str(comment_id)
        }

        res = self.client.delete(
            '/feed/delete_comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment deleted successfully.')

        post = db.find_post({"_id": self.post_id})

        self.assertEqual(post['number_of_comments'], 0)
        self.assertNotIn(comment_id, post['comments'])

    def test_delete_comment_with_no_commentid(self):
        """ Test delete comment. """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        comment_id = data['data']['_id']
        dump = {
            'post_id': str(self.post_id),
        }

        res = self.client.delete(
            '/feed/delete_comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 'Missing comment_id')

        post = db.find_post({"_id": self.post_id})

        self.assertEqual(post['number_of_comments'], 1)
        self.assertIn(ObjectId(comment_id), post['comments'])

    def test_delete_post_comment(self):
        """ Test deleting a post also
        deletes all the comments associated with this post """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        deleted = db.delete_post(self.post_id, self.user_id)
        comment = db.find_comment(data['data']['_id'], self.user_id)

        self.assertTrue(deleted)
        self.assertIsNone(comment)

    def test_delete_user_comment(self):
        """ Test deleting a user also
        deletes all the comments associated with this user """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comment created successfully.')

        deleted = db.delete_user(self.user_id)
        comment = db.find_comment(data['data']['_id'], self.user_id)

        self.assertTrue(deleted)
        self.assertIsNone(comment)

    def test_get_all_post_comments(self):
        """ Test get all comments asssociated with a post """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        dump = {
            'post_id': str(self.post_id),
            'body': 'Second Comment'
        }
        res_1 = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data_1 = res_1.get_json()

        dump = {
            'post_id': str(self.post_id),
            'body': 'First Comment'
        }
        res_2 = self.client.post(
            '/feed/comment', headers=headers, data=json.dumps(dump)
        )
        data_2 = res_2.get_json()

        self.assertEqual(res_1.status_code, 200)
        self.assertEqual(data_1['msg'], 'Comment created successfully.')

        self.assertEqual(res_2.status_code, 200)
        self.assertEqual(data_2['msg'], 'Comment created successfully.')

        dump = {
            'post_id': str(self.post_id),
        }
        res = self.client.get(
            '/feed/post_comments', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['msg'], 'Comments retrieved successfully.')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['body'], 'Second Comment')
        self.assertEqual(data['data'][1]['body'], 'First Comment')
