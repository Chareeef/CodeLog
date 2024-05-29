#!/usr/bin/env python3
"""Module to test the home page routes
"""
from bson import ObjectId
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from flask_jwt_extended import create_access_token
from routes.auth import store_token
from main import create_app
from time import sleep
import unittest


class TestCreateLog(unittest.TestCase):
    """Tests for 'POST /log' route
    """

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
            'email': 'dummy@yummy.choc',
            'password': 'gumbledore',
            'longest_streak': 0
        }
        cls.user_id = str(db.insert_user(infos))

        # Create JWT Access Token
        with cls.app.app_context():
            cls.access_token = create_access_token(
                identity=cls.user_id
            )

        # Store JWT Access Token
        store_token(
            cls.user_id,
            cls.access_token,
            cls.app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )

        # Define current streak ken in Redis
        cls.cs_key = 'albushog99_CS'

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def tearDown(self):
        """Reset streaks after each test
        """

        # Delete current streak key from Redis
        rc.delete(self.cs_key)

        # Reset longest streak to 0
        db.update_user_info(self.user_id, {'longest_streak': 0})

    def test_create_private_log(self):
        """Test posting a private entry
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'title': 'My post',
            'content': 'Here is my post'
        }

        response = self.client.post('/api/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertIn('_id', data)
        self.assertIn('user_id', data)
        self.assertIn('username', data)
        self.assertEqual(data.get('title'), 'My post')
        self.assertEqual(data.get('content'), 'Here is my post')
        self.assertEqual(data.get('is_public'), False)
        self.assertEqual(data.get('new_record'), True)
        self.assertNotIn('number_of_likes', data)
        self.assertNotIn('likes', data)
        self.assertNotIn('comments', data)
        self.assertAlmostEqual(data.get('datePosted'),
                               datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        # Verify that the log was stored in MongoDB
        post = db.find_post({'_id': ObjectId(data.get('_id'))})

        self.assertEqual(post.get('user_id'), data['user_id'])
        self.assertEqual(post.get('username'), data['username'])
        self.assertEqual(post.get('title'), data['title'])
        self.assertEqual(post.get('content'), data['content'])
        self.assertEqual(post.get('is_public'), data['is_public'])
        self.assertEqual(post.get('number_of_likes'), 0)
        self.assertEqual(post.get('likes'), [])
        self.assertEqual(post.get('comments'), [])
        self.assertEqual(post.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         data['datePosted'])

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 1)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 1)

    def test_create_public_log(self):
        """Test posting a public entry
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'title': 'My post',
            'content': 'Here is my post',
            'is_public': True
        }

        response = self.client.post('/api/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertIn('_id', data)
        self.assertIn('user_id', data)
        self.assertIn('username', data)
        self.assertEqual(data.get('title'), 'My post')
        self.assertEqual(data.get('content'), 'Here is my post')
        self.assertEqual(data.get('is_public'), True)
        self.assertEqual(data.get('new_record'), True)
        self.assertNotIn('number_of_likes', data)
        self.assertNotIn('likes', data)
        self.assertNotIn('comments', data)
        self.assertAlmostEqual(data.get('datePosted'),
                               datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        # Verify that the log was stored in MongoDB
        post = db.find_post({'_id': ObjectId(data.get('_id'))})

        self.assertEqual(post.get('user_id'), data['user_id'])
        self.assertEqual(post.get('username'), data['username'])
        self.assertEqual(post.get('title'), data['title'])
        self.assertEqual(post.get('content'), data['content'])
        self.assertEqual(post.get('is_public'), data['is_public'])
        self.assertEqual(post.get('number_of_likes'), 0)
        self.assertEqual(post.get('likes'), [])
        self.assertEqual(post.get('comments'), [])
        self.assertEqual(post.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         data['datePosted'])

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 1)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 1)

    def test_with_no_auth(self):
        """Test with no authentication
        """
        payload = {
            'title': 'My Post',
            'content': 'Here is my post'
        }

        response = self.client.post('/api/log', json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_with_wrong_auth(self):
        """Test with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        payload = {
            'title': 'My Post',
            'content': 'Here is my post'
        }

        response = self.client.post('/api/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_with_missing_title(self):
        """Test with missing title
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'content': 'Here is my post'
        }

        response = self.client.post('/api/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing title'})

    def test_with_missing_content(self):
        """Test with missing content
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'title': 'My post'
        }

        response = self.client.post('/api/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing content'})

    def test_create_log_with_wrong_is_public(self):
        """Test posting with a wrong is_public type
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}

        payload = {
            'title': 'My post 1',
            'content': 'Here is my post 1',
            'is_public': 'true'
        }

        response = self.client.post('/api/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': '`is_public` must be true or false'})

    def test_create_two_logs_in_correct_interval(self):
        """Test posting twice in different days
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}

        # First log
        payload1 = {
            'title': 'My post 1',
            'content': 'Here is my post 1'
        }

        response1 = self.client.post('/api/log', headers=headers, json=payload1)

        data1 = response1.get_json()

        # Pass to the next day
        sleep(2.1)

        # Second log
        payload2 = {
            'title': 'My post 2',
            'content': 'Here is my post 2'
        }

        response2 = self.client.post('/api/log', headers=headers, json=payload2)

        data2 = response2.get_json()

        # Verify responses
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 2)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 2)

    def test_create_two_logs_in_wrong_interval(self):
        """Test posting twice in the same day
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}

        # First log
        payload1 = {
            'title': 'My post 1',
            'content': 'Here is my post 1'
        }

        response1 = self.client.post('/api/log', headers=headers, json=payload1)

        # Second log
        payload2 = {
            'title': 'My post 2',
            'content': 'Here is my post 2'
        }

        response2 = self.client.post('/api/log', headers=headers, json=payload2)

        data2 = response2.get_json()

        # Verify responses
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(data2, {'error': 'Only one post per day is allowed'})

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 1)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 1)

    def test_loosing_current_streak(self):
        """Test loosing current streak
        """

        # Cheating for testing is not cheating
        db.update_user_info(self.user_id, {'longest_streak': 4})
        rc.psetex(self.cs_key, 1900, 4)

        headers = {'Authorization': 'Bearer ' + self.access_token}

        # First log
        payload1 = {
            'title': 'My post 1',
            'content': 'Here is my post 1'
        }

        response1 = self.client.post('/api/log', headers=headers, json=payload1)

        data1 = response1.get_json()

        # Verify response
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(data1.get('new_record'), True)

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 5)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 5)

        # Skip a day
        sleep(4.1)

        # Ensure current streak is dead
        self.assertIsNone(rc.get(self.cs_key))

        # Second log
        payload2 = {
            'title': 'My post 2',
            'content': 'Here is my post 2'
        }

        response2 = self.client.post('/api/log', headers=headers, json=payload2)

        data2 = response2.get_json()

        # Verify response
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(data2.get('new_record'), False)

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 1)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 5)
