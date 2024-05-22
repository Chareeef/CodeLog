#!/usr/bin/env python3
"""Module to test the user space routes
"""
from bson import ObjectId
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from db.db_manager import hash_pass, check_hash_password
from flask_jwt_extended import create_access_token
from routes.auth import store_token
from main import create_app
import string
import random
import unittest


class TestGetInfos(unittest.TestCase):
    """Tests for 'GET /me/get_infos' route
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

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def test_get_infos_with_no_token(self):
        """Test getting infos with no authentication
        """
        response = self.client.get('/me/get_infos')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_infos_with_wrong_token(self):
        """Test getting user's infos with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        response = self.client.get('/me/get_infos', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_get_infos_initially(self):
        """Test getting a fresh user's infos
        """
        response = self.client.get('/me/get_infos', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'email': 'dummy@yummy.choc',
            'username': 'albushog99'
        })


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

    def test_get_streaks_with_no_token(self):
        """Test getting streaks with no authentication
        """
        response = self.client.get('/me/streaks')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_streaks_with_wrong_token(self):
        """Test getting user's streaks with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        response = self.client.get('/me/streaks', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_get_streaks_initially(self):
        """Test getting a fresh user's streaks
        """
        response = self.client.get('/me/streaks', headers={
            'Authorization': 'Bearer ' + self.access_token
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
            'Authorization': 'Bearer ' + self.access_token
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

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def test_update_infos_with_wrong_token(self):
        """Test updating user's infos with wrong authentication
        """
        response = self.client.put('/me/update_infos')
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_update_infos_with_wrong_token(self):
        """Test updating user's infos with wrong authentication
        """
        response = self.client.put('/me/update_infos', headers={
            'Authorization': 'Bearer ' + self.access_token + '123'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_update_infos_with_wrong_field(self):
        """Test updating a wrong field
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
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
        headers = {'Authorization': 'Bearer ' + self.access_token}
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


class TestUpdatePassword(unittest.TestCase):
    """Tests for 'PUT /me/update_password' route
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
            'email': 'expeliamus@poud.mgc',
            'password': 'gumbledore',
            'longest_streak': 0
        }

        cls.user_id = str(db.insert_user(infos))
        cls.user_email = infos['email']

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

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def tearDown(self):
        """Reset password to 'gumbledore'
        """
        new_hashed_password = hash_pass('gumbledore')
        db._db['users'].find_one_and_update(
            {'_id': ObjectId(self.user_id)},
            {'$set': {'password': new_hashed_password}}
        )

    def test_update_password_with_no_token(self):
        """Test updating user's password with no authentication
        """
        response = self.client.put('/me/update_password')
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_update_password_with_wrong_token(self):
        """Test updating user's password with wrong authentication
        """
        response = self.client.put('/me/update_password', headers={
            'Authorization': 'Bearer ' + self.access_token + '123'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_update_password_successfully(self):
        """Test updating user's password successfully
        """
        headers = {'Authorization': f'Bearer {self.access_token}'}
        payload = {'old_password': 'gumbledore', 'new_password': 'phoenix3000'}
        response = self.client.put(
            '/me/update_password', headers=headers, json=payload)
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'success': 'password updated'})

        # Verify updated password in DB
        hashed_password = db.get_hash(self.user_email)
        self.assertTrue(check_hash_password(hashed_password, 'phoenix3000'))

    def test_update_password_with_missing_old_pwd(self):
        """Test updating user's password with missing old password
        """
        headers = {'Authorization': f'Bearer {self.access_token}'}
        payload = {'new_password': 'gandalf'}
        response = self.client.put(
            '/me/update_password', headers=headers, json=payload)
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing old password'})

    def test_update_password_with_missing_new_pwd(self):
        """Test updating user's password with missing new password
        """
        headers = {'Authorization': f'Bearer {self.access_token}'}
        payload = {'old_password': 'gumbledore'}
        response = self.client.put(
            '/me/update_password', headers=headers, json=payload)
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing new password'})

    def test_update_password_with_wrong_old_pwd(self):
        """Test updating user's password with wrong old password
        """
        headers = {'Authorization': f'Bearer {self.access_token}'}
        payload = {'old_password': 'phoenix3000', 'new_password': 'gandalf'}
        response = self.client.put(
            '/me/update_password', headers=headers, json=payload)
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'wrong old password'})


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
        cls.user_id = db.insert_user(infos)

        # Create JWT Access Token
        with cls.app.app_context():
            cls.access_token = create_access_token(
                identity=str(cls.user_id)
            )

        # Store JWT Access Token
        store_token(
            str(cls.user_id),
            cls.access_token,
            cls.app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )

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

            post['user_id'] = cls.user_id
            db.insert_post(post)

        # Sort posts
        cls.posts.sort(key=lambda x: x['title'])

        # Stringify datePosted
        for p in cls.posts:
            p['datePosted'] = p['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db.clear_db()

    def test_get_posts_with_no_token(self):
        """Test getting posts with no authentication
        """
        response = self.client.get('/me/posts')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_posts_with_wrong_token(self):
        """Test getting posts with wrong authentication
        """
        response = self.client.get('/me/posts', headers={
            'Authorization': 'Bearer ' + self.access_token + 'k'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_get_posts(self):
        """Test successefully getting posts
        """
        response = self.client.get('/me/posts', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)

        # Sort data
        data.sort(key=lambda x: x['title'])

        self.assertEqual(len(self.posts), len(data))

        for data_dict, expected_dict in zip(data, self.posts):
            self.assertDictEqual(data_dict, expected_dict)
