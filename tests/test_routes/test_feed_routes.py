#!/usr/bin/env python3
"""Module to test the Authentication route
"""
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from db.db_manager import check_hash_password
from main import create_app
import unittest
from bson import ObjectId
import json


class FeedTests(unittest.TestCase):
    """ Tests for authenticated users """

    def setUp(self):
        """ Runs once before every test """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        info = {
            'email': 'mohamed@example.com',
            'username': 'mohamed',
            'password': 'pass123',
            'current_streak': 0,
            'longest_streak': 0
        }

        self.user_id = db.insert_user(info)

        self.post_info = {
            'user_id': ObjectId(),
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

        post = db.find_post({'_id': self.post_id})

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

        post = db.find_post({'_id': self.post_id})

        self.assertEqual(post['number_of_likes'], 1)
        self.assertIn(self.user_id, post['likes'])

        res = self.client.post(
            '/feed/like', headers=headers, data=json.dumps(dump)
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, {'error': 'User has already liked the post.'})

        post = db.find_post({'_id': self.post_id})

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

        post = db.find_post(dummy_id, self.user_id)

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
