#!/usr/bin/env python3
"""Module to test the user space routes
"""
from bson import ObjectId
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
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
            is_public = random.choice([True, False])
            datePosted = datetime.utcnow()

            post = {
                'title': title,
                'content': content,
                'is_public': is_public,
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

        # Create dummy malicious user
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

        response = self.client.put('/me/update_post', json=payload)

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

        response = self.client.put('/me/update_post', headers=headers, json=payload)

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

        response = self.client.put('/me/update_post', headers=headers, json=payload)

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

        response = self.client.put('/me/update_post', headers=headers, json=payload)

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

        response = self.client.put('/me/update_post', headers=headers, json=payload)

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

        response = self.client.put('/me/update_post', headers=headers, json=payload)

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

        response = self.client.put('/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': '`is_public` must be true or false'})

    def test_update_public_post(self):
        """Test updating post 1
        """

        # Check post 1
        post1 = db.find_post({'_id': ObjectId(self.post_id1)})

        self.assertEqual(post1.get('user_id'), self.user_id)
        self.assertEqual(post1.get('title'), 'Old title 1')
        self.assertEqual(post1.get('content'), 'Old content 1')
        self.assertEqual(post1.get('is_public'), True)
        #self.assertEqual(post2.get('number_of_likes'), 0)
        #self.assertEqual(post2.get('likes'), [])
        #self.assertEqual(post2.get('comments'), [])
        self.assertEqual(post1.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         self.datePosted1)

        # Make call
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'post_id': self.post_id1,
            'title': 'New title 1',
            'content': 'New content 1'
        }

        response = self.client.put('/me/update_post', headers=headers, json=payload)

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
        #self.assertEqual(new_post2.get('number_of_likes'), 0)
        #self.assertEqual(new_post2.get('likes'), [])
        #self.assertEqual(new_post2.get('comments'), [])
        self.assertEqual(new_post1.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         self.datePosted1)

    def test_update_private_post(self):
        """Test updating post 2
        """

        # Check post 2
        post2 = db.find_post({'_id': ObjectId(self.post_id2)})
        print(post2)

        self.assertEqual(post2.get('user_id'), self.user_id)
        self.assertEqual(post2.get('title'), 'Old title 2')
        self.assertEqual(post2.get('content'), 'Old content 2')
        self.assertEqual(post2.get('is_public'), False)
        #self.assertEqual(post2.get('number_of_likes'), 0)
        #self.assertEqual(post2.get('likes'), [])
        #self.assertEqual(post2.get('comments'), [])
        self.assertEqual(post2.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         self.datePosted2)

        # Make call
        headers = {'Authorization': 'Bearer ' + self.access_token}
        payload = {
            'post_id': self.post_id2,
            'title': 'New title 2',
            'content': 'New content 2',
            'is_public': True
        }
        print(db.find_all_posts(), '--\n')
        response = self.client.put('/me/update_post', headers=headers, json=payload)

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'success': 'post updated'})

        # Recheck post 2
        new_post2 = db.find_post({'_id': ObjectId(self.post_id2)})
        print('new_post2:', new_post2)
        print(db.find_all_posts(), '--\n')

        self.assertEqual(new_post2.get('user_id'), self.user_id)
        self.assertEqual(new_post2.get('title'), 'New title 2')
        self.assertEqual(new_post2.get('content'), 'New content 2')
        self.assertEqual(new_post2.get('is_public'), True)
        #self.assertEqual(new_post2.get('number_of_likes'), 0)
        #self.assertEqual(new_post2.get('likes'), [])
        #self.assertEqual(new_post2.get('comments'), [])
        self.assertEqual(new_post2.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         self.datePosted2)
