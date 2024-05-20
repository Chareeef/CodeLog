#!/usr/bin/env python3
"""Module to test the user space routes
"""
import base64
from bson import ObjectId
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from main import create_app
import string
import random
import unittest


class TestGetStreaks(unittest.TestCase):
    """Tests for 'GET /me/streaks' route
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

        # Store token in redis
        rc.set(cls.token, cls.user_id)

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

    def test_get_streaks_with_wrong_token(self):
        """Test getting user's streaks with wrong authentication
        """
        response = self.client.get('/me/streaks', headers={
            'Y-Token': self.token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Unauthorized'})

    def test_get_streaks_initially(self):
        """Test getting a fresh user's streaks
        """
        response = self.client.get('/me/streaks', headers={
            'X-Token': self.token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'longest_streak': 0, 'current_streak': 0})

    def test_get_streaks_of_a_disciplined_user(self):
        """Test getting a disciplined user's streaks
        """

        # As they say: cheating while testing is not cheating
        db.update_user_info(self.user_id, {'longest_streak': 69})
        rc.setex(self.cs_key, 2, 48)

        response = self.client.get('/me/streaks', headers={
            'X-Token': self.token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'longest_streak': 69, 'current_streak': 48})


class TestUpdateInfos(unittest.TestCase):
    """Tests for 'PUT /me/update_infos' route
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

        # Store the token in redis
        rc.set(cls.token, cls.user_id)

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def test_update_infos_with_wrong_token(self):
        """Test updating user's infos with wrong authentication
        """
        response = self.client.put('/me/update_infos', headers={
            'X-Token': self.token + '123'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Unauthorized'})

    def test_update_infos_with_wrong_field(self):
        """Test updating a wrong field
        """
        headers = {'X-Token': self.token}
        to_update = {'email': 'albus@poud.com',
                     'username': 'phoenix00',
                     'age': 348
                     }
        response = self.client.put('/me/update_infos',
                                   headers=headers,
                                   json=to_update)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Only update email and/or username'})

    def test_update_email_and_username(self):
        """Test successefully updating user's email and username
        """
        headers = {'X-Token': self.token}
        to_update = {'email': 'albus@poud.com', 'username': 'phoenix00'}
        response = self.client.put('/me/update_infos',
                                   headers=headers,
                                   json=to_update)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'success': 'user updated'})

        # Ensure the user was updated
        user = db.find_user({'_id': ObjectId(self.user_id)})
        self.assertEqual(user['email'], to_update['email'])
        self.assertEqual(user['username'], to_update['username'])


class TestGetPosts(unittest.TestCase):
    """Tests for 'GET /user/posts' route
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
        user_id = db.insert_user(infos)

        # Create Authentication token
        data_to_encode = 'dummy@yummy.choc:gumbledore'
        b64_string = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        cls.token = 'auth_64' + b64_string

        # Store in redis for 5 seconds
        rc.setex(cls.token, 5, str(user_id))

        # Create dummy posts
        cls.posts = []

        for _ in range(3):
            characters = string.ascii_letters + string.punctuation

            title = ''.join(random.choice(characters) for _ in range(10))
            content = ''.join(random.choice(characters) for _ in range(30))
            isPublic = random.choice([True, False])
            datePosted = datetime.utcnow()

            post = {
                'title': title,
                'content': content,
                'isPublic': isPublic,
                'datePosted': datePosted
            }

            cls.posts.append(post.copy())

            post['user_id'] = user_id
            db.insert_post(post)

        # Sort cls.posts
        cls.posts.sort(key=lambda x: x['title'])

        # Stringify datePosted
        for p in cls.posts:
            p['datePosted'] = p['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db.clear_db()

    def test_get_posts_with_wrong_token(self):
        """Test getting posts with wrong authentication
        """
        response = self.client.get('/me/posts', headers={
            'X-Token': self.token + 'k'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Unauthorized'})

    def test_get_posts(self):
        """Test successefully getting posts
        """
        response = self.client.get('/me/posts', headers={
            'X-Token': self.token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)

        # Sort data
        data.sort(key=lambda x: x['title'])

        self.assertEqual(len(self.posts), len(data))

        for data_dict, expected_dict in zip(data, self.posts):
            self.assertDictEqual(data_dict, expected_dict)
