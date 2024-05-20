#!/usr/bin/env python3
"""Module to test the home page routes
"""
import base64
from bson import ObjectId
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from main import create_app
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

        # Create Authentication token
        data_to_encode = 'dummy@yummy.choc:gumbledore'
        b64_string = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        cls.token = 'auth_64' + b64_string

        # Store in redis for 5 seconds
        rc.setex(cls.token, 5, cls.user_id)

        # Define current streak ken in Redis
        cls.cs_key = 'albushog99_CS'

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db.clear_db()

    def tearDown(self):
        """Delete current streak key from Redis after each test
        """
        rc.delete(self.cs_key)

        # Reset longest streak to 0
        db.update_user_info(self.user_id, {'longest_streak': 0})

    def test_create_private_log(self):
        """Test posting a private entry
        """
        headers = {'X-Token': self.token}
        payload = {
            'title': 'My post',
            'content': 'Here is my post'
        }

        response = self.client.post('/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertIn('_id', data)
        self.assertIn('user_id', data)
        self.assertEqual(data.get('title'), 'My post')
        self.assertEqual(data.get('content'), 'Here is my post')
        self.assertEqual(data.get('is_public'), False)
        self.assertEqual(data.get('new_record'), True)
        self.assertEqual(data.get('datePosted'),
                         datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        # Verify that the log was stored in MongoDB
        post = db.find_post({'_id': ObjectId(data.get('_id'))})

        self.assertEqual(post.get('user_id'), data['user_id'])
        self.assertEqual(post.get('title'), data['title'])
        self.assertEqual(post.get('content'), data['content'])
        self.assertEqual(post.get('is_public'), data['is_public'])
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
        headers = {'X-Token': self.token}
        payload = {
            'title': 'My post',
            'content': 'Here is my post',
            'is_public': True
        }

        response = self.client.post('/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertIn('_id', data)
        self.assertIn('user_id', data)
        self.assertEqual(data.get('title'), 'My post')
        self.assertEqual(data.get('content'), 'Here is my post')
        self.assertEqual(data.get('is_public'), True)
        self.assertEqual(data.get('datePosted'),
                         datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        # Verify that the log was stored in MongoDB
        post = db.find_post({'_id': ObjectId(data.get('_id'))})

        self.assertEqual(post.get('user_id'), data['user_id'])
        self.assertEqual(post.get('title'), data['title'])
        self.assertEqual(post.get('content'), data['content'])
        self.assertEqual(post.get('is_public'), data['is_public'])
        self.assertEqual(post.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         data['datePosted'])

        # Verify current streak
        self.assertEqual(int(rc.get(self.cs_key).decode('utf-8')), 1)

        # Verify longest streak
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['longest_streak'], 1)

    def test_with_wrong_auth(self):
        """Test with wrong authentication
        """
        headers = {'X-Token': self.token + '123'}
        payload = {
            'title': 'My Post',
            'content': 'Here is my post'
        }

        response = self.client.post('/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Unauthorized'})

    def test_with_missing_title(self):
        """Test with missing title
        """
        headers = {'X-Token': self.token}
        payload = {
            'content': 'Here is my post'
        }

        response = self.client.post('/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing title'})

    def test_with_missing_content(self):
        """Test with missing content
        """
        headers = {'X-Token': self.token}
        payload = {
            'title': 'My post'
        }

        response = self.client.post('/log', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing content'})

    def test_create_two_logs(self):
        """Test posting twice in the same day
        """
        headers = {'X-Token': self.token}

        payload1 = {
            'title': 'My post 1',
            'content': 'Here is my post 1'
        }

        response1 = self.client.post('/log', headers=headers, json=payload1)

        payload2 = {
            'title': 'My post 2',
            'content': 'Here is my post 2'
        }

        response2 = self.client.post('/log', headers=headers, json=payload2)

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
