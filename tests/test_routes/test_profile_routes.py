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
            'email': 'dummy@yummy.choc',
            'password': 'gumbledore',
            'full_name': 'Albus Dumbledore',
            'current_streak': 0,
            'longest_streak': 0
        }
        userId = db.insert_user(infos).inserted_id

        # Create Authentication token
        data_to_encode = 'dummy@yummy.choc:gumbledore'
        b64_string = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        cls.token = 'auth_64' + b64_string

        # Store in redis for 5 seconds
        rc.setex(cls.token, 5, str(userId))

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

            post['userId'] = userId
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
        db._db['users'].delete_many({})
        db._db['posts'].delete_many({})

    def test_get_posts(self):
        """Test successefully getting posts
        """
        response = self.client.get('/user/posts', headers={
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
