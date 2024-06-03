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
from time import sleep
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
            'email': 'lumos@poud.mgc',
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
        response = self.client.get('/api/me/get_infos')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_infos_with_wrong_token(self):
        """Test getting user's infos with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        response = self.client.get('/api/me/get_infos', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_get_infos_initially(self):
        """Test getting a fresh user's infos
        """
        response = self.client.get('/api/me/get_infos', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'email': 'lumos@poud.mgc',
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
            'email': 'lumos@poud.mgc',
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
        response = self.client.get('/api/me/streaks')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_streaks_with_wrong_token(self):
        """Test getting user's streaks with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        response = self.client.get('/api/me/streaks', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_get_streaks_initially(self):
        """Test getting a fresh user's streaks
        """
        response = self.client.get('/api/me/streaks', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'longest_streak': 0,
                                'current_streak': 0, 'ttl': 0})

    def test_get_streaks_of_a_disciplined_user(self):
        """Test getting a disciplined user's streaks
        """

        # As they say: cheating while testing is not cheating
        db.update_user_info(self.user_id, {'longest_streak': 69})
        rc.setex(self.cs_key, 2, 48)

        response = self.client.get('/api/me/streaks', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'longest_streak': 69,
                                'current_streak': 48, 'ttl': 2})


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
            'email': 'lumos@poud.mgc',
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
        response = self.client.put('/api/me/update_infos')
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_update_infos_with_wrong_token(self):
        """Test updating user's infos with wrong authentication
        """
        response = self.client.put('/api/me/update_infos', headers={
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
        response = self.client.put('/api/me/update_infos',
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
        response = self.client.put('/api/me/update_infos',
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
        response = self.client.put('/api/me/update_password')
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_update_password_with_wrong_token(self):
        """Test updating user's password with wrong authentication
        """
        response = self.client.put('/api/me/update_password', headers={
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
            '/api/me/update_password', headers=headers, json=payload)
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
            '/api/me/update_password', headers=headers, json=payload)
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
            '/api/me/update_password', headers=headers, json=payload)
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
            '/api/me/update_password', headers=headers, json=payload)
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
            'email': 'lumos@poud.mgc',
            'password': 'gumbledore',
            'longest_streak': 0
        }
        user_id = str(db.insert_user(infos))

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
        cls.posts = []

        for _ in range(3):
            characters = string.ascii_letters + string.punctuation

            title = ''.join(random.choice(characters) for _ in range(10))
            content = ''.join(random.choice(characters) for _ in range(30))
            is_public = random.choice([True, False])
            datePosted = datetime.utcnow()

            post = {
                'username': infos['username'],
                'title': title,
                'content': content,
                'is_public': is_public,
                'likes': [],
                'number_of_likes': 0,
                'comments': [],
                'number_of_comments': 0,
                'datePosted': datePosted
            }

            cls.posts.append(post.copy())

            post['user_id'] = user_id
            db.insert_post(post)

        # Sort posts from the most to the less recent
        cls.posts.sort(key=lambda x: x['datePosted'], reverse=True)

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
        response = self.client.get('/api/me/posts')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_get_posts_with_wrong_token(self):
        """Test getting posts with wrong authentication
        """
        response = self.client.get('/api/me/posts', headers={
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
        response = self.client.get('/api/me/posts', headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(self.posts), len(data))

        for data_dict, expected_dict in zip(data, self.posts):
            self.assertDictEqual(data_dict, expected_dict)


class TestUpdateLog(unittest.TestCase):
    """Tests for 'PUT /me/update_post' route
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
            'email': 'lumos@poud.mgc',
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

        # Create dummy malicious user
        infos = {
            'username': 'tomdemort67',
            'email': 'riddle@poud.mgc',
            'password': 'serpentard',
            'longest_streak': 0
        }
        cls.dark_user_id = str(db.insert_user(infos))

        # Create JWT malicious Access Token
        with cls.app.app_context():
            cls.dark_access_token = create_access_token(
                identity=cls.dark_user_id
            )

        # Store JWT malicious Access Token
        store_token(
            cls.dark_user_id,
            cls.dark_access_token,
            cls.app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )

        # Create two dummy posts
        doc1 = {
            'user_id': cls.user_id,
            'title': 'Old title 1',
            'content': 'Old content 1',
            'is_public': True,
            'number_of_likes': 0,
            'likes': [],
            'comments': [],
            'datePosted': datetime.utcnow()
        }

        cls.post_id1 = str(db.insert_post(doc1))
        cls.datePosted1 = doc1['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

        sleep(2)

        doc2 = {
            'user_id': cls.user_id,
            'title': 'Old title 2',
            'content': 'Old content 2',
            'is_public': False,
            'number_of_likes': 0,
            'likes': [],
            'comments': [],
            'datePosted': datetime.utcnow()
        }

        cls.post_id2 = str(db.insert_post(doc2))
        cls.datePosted2 = doc2['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def test_with_no_auth(self):
        """Test with no authentication
        """
        payload = {
            'post_id': self.post_id1,
            'title': 'My Post',
            'content': 'Here is my post'
        }

        response = self.client.put('/api/me/update_post', json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_with_wrong_auth(self):
        """Test with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        payload = {
            'post_id': self.post_id1,
            'title': 'My Post',
            'content': 'Here is my post'
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_with_missing_post_id(self):
        """Test with missing post_id
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'title': 'My post',
            'content': 'Here is my post'
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing post_id'})

    def test_updating_another_user_post(self):
        """Test updating another user's post
        """
        headers = {'Authorization': 'Bearer ' + self.dark_access_token}
        payload = {
            'post_id': self.post_id1,
            'title': 'My post',
            'content': 'Here is my post'
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'You have no post with this post_id'})

    def test_with_missing_title(self):
        """Test with missing title
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'post_id': self.post_id1,
            'content': 'Here is my post'
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing title'})

    def test_with_missing_content(self):
        """Test with missing content
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'post_id': self.post_id1,
            'title': 'My post',
            'content': ''
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing content'})

    def test_update_post_with_wrong_is_public(self):
        """Test updating a post with a wrong is_public type
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}

        payload = {
            'post_id': self.post_id1,
            'title': 'My post 1',
            'content': 'Here is my post 1',
            'is_public': 'true'
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': '`is_public` must be true or false'})

    def test_update_public_post(self):
        """Test updating post 1
        """

        time_fmt = '%Y/%m/%d %H:%M:%S'

        # Check post 1
        post1 = db.find_post({'_id': ObjectId(self.post_id1)})

        self.assertEqual(post1.get('user_id'), self.user_id)
        self.assertEqual(post1.get('title'), 'Old title 1')
        self.assertEqual(post1.get('content'), 'Old content 1')
        self.assertEqual(post1.get('is_public'), True)
        self.assertEqual(post1.get('number_of_likes'), 0)
        self.assertEqual(post1.get('likes'), [])
        self.assertEqual(post1.get('comments'), [])
        self.assertEqual(post1.get('datePosted').strftime(time_fmt),
                         self.datePosted1)

        # Make call
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'post_id': self.post_id1,
            'title': 'New title 1',
            'content': 'New content 1'
        }

        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'success': 'post updated'})

        # Recheck post 1
        new_post1 = db.find_post({'_id': ObjectId(self.post_id1)})

        self.assertEqual(new_post1.get('user_id'), self.user_id)
        self.assertEqual(new_post1.get('title'), 'New title 1')
        self.assertEqual(new_post1.get('content'), 'New content 1')
        self.assertEqual(new_post1.get('is_public'), True)
        self.assertEqual(new_post1.get('number_of_likes'), 0)
        self.assertEqual(new_post1.get('likes'), [])
        self.assertEqual(new_post1.get('comments'), [])
        self.assertEqual(new_post1.get('datePosted').strftime(time_fmt),
                         self.datePosted1)

    def test_update_private_post(self):
        """Test updating post 2
        """

        time_fmt = '%Y/%m/%d %H:%M:%S'

        # Check post 2
        post2 = db.find_post({'_id': ObjectId(self.post_id2)})

        self.assertEqual(post2.get('user_id'), self.user_id)
        self.assertEqual(post2.get('title'), 'Old title 2')
        self.assertEqual(post2.get('content'), 'Old content 2')
        self.assertEqual(post2.get('is_public'), False)
        self.assertEqual(post2.get('number_of_likes'), 0)
        self.assertEqual(post2.get('likes'), [])
        self.assertEqual(post2.get('comments'), [])
        self.assertEqual(post2.get('datePosted').strftime(time_fmt),
                         self.datePosted2)

        # Make call
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'post_id': self.post_id2,
            'title': 'New title 2',
            'content': 'New content 2',
            'is_public': True
        }
        response = self.client.put(
            '/api/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'success': 'post updated'})

        # Recheck post 2
        new_post2 = db.find_post({'_id': ObjectId(self.post_id2)})

        self.assertEqual(new_post2.get('user_id'), self.user_id)
        self.assertEqual(new_post2.get('title'), 'New title 2')
        self.assertEqual(new_post2.get('content'), 'New content 2')
        self.assertEqual(new_post2.get('is_public'), True)
        self.assertEqual(new_post2.get('number_of_likes'), 0)
        self.assertEqual(new_post2.get('likes'), [])
        self.assertEqual(new_post2.get('comments'), [])
        self.assertEqual(new_post2.get('datePosted').strftime(time_fmt),
                         self.datePosted2)


class TestDeleteLog(unittest.TestCase):
    """Tests for 'DELETE /me/delete_post' route
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
            'email': 'lumos@poud.mgc',
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

        # Create dummy malicious user
        infos = {
            'username': 'tomdemort67',
            'email': 'riddle@poud.mgc',
            'password': 'serpentard',
            'longest_streak': 0
        }
        cls.dark_user_id = str(db.insert_user(infos))

        # Create JWT malicious Access Token
        with cls.app.app_context():
            cls.dark_access_token = create_access_token(
                identity=cls.dark_user_id
            )

        # Store JWT malicious Access Token
        store_token(
            cls.dark_user_id,
            cls.dark_access_token,
            cls.app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )

        # Create two dummy posts
        doc1 = {
            'user_id': cls.user_id,
            'title': 'title 1',
            'content': 'content 1',
            'is_public': True,
            'number_of_likes': 0,
            'likes': [],
            'comments': [],
            'datePosted': datetime.utcnow()
        }

        cls.post_id1 = str(db.insert_post(doc1))

        doc2 = {
            'user_id': cls.user_id,
            'title': 'title 2',
            'content': 'content 2',
            'is_public': False,
            'number_of_likes': 0,
            'likes': [],
            'comments': [],
            'datePosted': datetime.utcnow()
        }

        cls.post_id2 = str(db.insert_post(doc2))

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def test_with_no_auth(self):
        """Test with no authentication
        """
        payload = {
            'post_id': self.post_id1
        }

        response = self.client.delete('/api/me/delete_post', json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_with_wrong_auth(self):
        """Test with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}
        payload = {
            'post_id': self.post_id1
        }

        response = self.client.delete(
            '/api/me/delete_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_with_missing_post_id(self):
        """Test with missing post_id
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}

        response = self.client.delete(
            '/api/me/delete_post', headers=headers, json={})

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing post_id'})

    def test_deleting_another_user_post(self):
        """Test deleting another user's post
        """
        headers = {'Authorization': 'Bearer ' + self.dark_access_token}
        payload = {
            'post_id': self.post_id1
        }

        response = self.client.delete(
            '/api/me/delete_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'You have no post with this post_id'})

    def test_delete_post_successfully(self):
        """Test deleting posts
        """
        headers = {'Authorization': 'Bearer ' + self.access_token}

        # Check users' posts number
        self.assertEqual(len(db.find_user_posts(self.user_id)), 2)

        # Check post 1 exístence
        self.assertIsNotNone(db.find_post({'_id': ObjectId(self.post_id1)}))

        # Delet post 1
        payload1 = {
            'post_id': self.post_id1
        }

        response1 = self.client.delete(
            '/api/me/delete_post', headers=headers, json=payload1)

        data1 = response1.get_json()

        # Verify response
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(data1, {'success': 'deleted post'})

        # Check post 1 inexístence
        self.assertIsNone(db.find_post({'_id': ObjectId(self.post_id1)}))

        # Recheck users' posts number
        self.assertEqual(len(db.find_user_posts(self.user_id)), 1)

        # Check post 2 exístence
        self.assertIsNotNone(db.find_post({'_id': ObjectId(self.post_id2)}))

        # Delet post 2
        payload2 = {
            'post_id': self.post_id2
        }

        response2 = self.client.delete(
            '/api/me/delete_post', headers=headers, json=payload2)

        data2 = response2.get_json()

        # Verify response
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(data2, {'success': 'deleted post'})

        # Check post 2 inexístence
        self.assertIsNone(db.find_post({'_id': ObjectId(self.post_id2)}))

        # Check user's posts were all deleted
        self.assertEqual(len(db.find_user_posts(self.user_id)), 0)


class TestDeleteUser(unittest.TestCase):
    """Tests for 'DELETE /me/delete_user' route
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
            'email': 'lumos@poud.mgc',
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

        # Create another dummy user
        infos = {
            'username': 'tomdemort67',
            'email': 'riddle@poud.mgc',
            'password': 'serpentard',
            'longest_streak': 0
        }
        cls.another_user_id = str(db.insert_user(infos))

        # Create another JWT Access Token
        with cls.app.app_context():
            cls.another_access_token = create_access_token(
                identity=cls.another_user_id
            )

        # Store another JWT Access Token
        store_token(
            cls.another_user_id,
            cls.another_access_token,
            cls.app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )

        # Create two dummy posts for the first user
        doc1 = {
            'user_id': cls.user_id,
            'title': 'title 1',
            'content': 'content 1',
            'is_public': True,
            'number_of_likes': 0,
            'likes': [],
            'comments': [],
            'datePosted': datetime.utcnow()
        }

        db.insert_post(doc1)

        doc2 = {
            'user_id': cls.user_id,
            'title': 'title 2',
            'content': 'content 2',
            'is_public': False,
            'number_of_likes': 0,
            'likes': [],
            'comments': [],
            'datePosted': datetime.utcnow()
        }

        db.insert_post(doc2)

    @classmethod
    def tearDownClass(cls):
        """Clear Mongo and Redis databases
        """
        db.clear_db()
        rc.flushdb()

    def test_with_no_auth(self):
        """Test with no authentication
        """
        response = self.client.delete('/api/me/delete_user')

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_with_wrong_auth(self):
        """Test with wrong authentication
        """
        headers = {'Authorization': 'Bearer ' + self.access_token[:-2] + 'o3'}

        response = self.client.delete('/api/me/delete_user', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'})

    def test_delete_user_having_posts(self):
        """Test deleting a user having some posts
        """

        # Check the existence of the user and the user's posts
        self.assertIsNotNone(db.find_user({'_id': ObjectId(self.user_id)}))
        self.assertEqual(len(db.find_user_posts(self.user_id)), 2)

        # Make the call
        headers = {'Authorization': 'Bearer ' + self.access_token}

        response = self.client.delete('/api/me/delete_user', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'success': 'account deleted'})

        # Check the deletion of the user and the user's posts
        self.assertIsNone(db.find_user({'_id': ObjectId(self.user_id)}))
        self.assertEqual(len(db.find_user_posts(self.user_id)), 0)

    def test_delete_user_with_no_posts(self):
        """Test deleting a user having no posts
        """

        # Check the existence of the user and the absence of user's posts
        self.assertIsNotNone(db.find_user(
            {'_id': ObjectId(self.another_user_id)}))
        self.assertEqual(len(db.find_user_posts(self.another_user_id)), 0)

        # Make the call
        headers = {'Authorization': 'Bearer ' + self.another_access_token}

        response = self.client.delete('/api/me/delete_user', headers=headers)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'success': 'account deleted'})

        # Check the user's deletion of the user
        self.assertIsNone(db.find_user(
            {'_id': ObjectId(self.another_user_id)}))

        # Check that the user's posts are always absent
        self.assertEqual(len(db.find_user_posts(self.another_user_id)), 0)
