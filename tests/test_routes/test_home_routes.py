#!/usr/bin/env python3
"""Module to test the home page routes
"""
from bson import ObjectId
from config import TestConfig
from datetime import datetime
from db import db
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

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db.clear_db()

    def test_create_private_log(self):
        """Test posting a private entry
        """
        response = self.client.post('/log', json={
            'title': 'My post',
            'content': 'Here is my post'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertIn('_id', data)
        self.assertIn('user_id', data)
        self.assertEqual(data.get('title'), 'My post')
        self.assertEqual(data.get('content'), 'Here is my post')
        self.assertEqual(data.get('isPublic'), False)
        self.assertEqual(data.get('datePosted'),
                         datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        # Verify that the log was stored in MongoDB
        post = db.find_post({'_id': ObjectId(data.get('_id'))})

        # TODO: Use ObjectId
        self.assertEqual(post.get('user_id'), data['user_id'])
        self.assertEqual(post.get('title'), data['title'])
        self.assertEqual(post.get('content'), data['content'])
        self.assertEqual(post.get('isPublic'), data['isPublic'])
        self.assertEqual(post.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         data['datePosted'])

    def test_create_public_log(self):
        """Test posting a public entry
        """
        response = self.client.post('/log', json={
            'title': 'My post',
            'content': 'Here is my post',
            'isPublic': True
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 201)
        self.assertIn('_id', data)
        self.assertIn('user_id', data)
        self.assertEqual(data.get('title'), 'My post')
        self.assertEqual(data.get('content'), 'Here is my post')
        self.assertEqual(data.get('isPublic'), True)
        self.assertEqual(data.get('datePosted'),
                         datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        # Verify that the log was stored in MongoDB
        post = db.find_post({'_id': ObjectId(data.get('_id'))})

        # TODO: Use ObjectId
        self.assertEqual(post.get('user_id'), data['user_id'])
        self.assertEqual(post.get('title'), data['title'])
        self.assertEqual(post.get('content'), data['content'])
        self.assertEqual(post.get('isPublic'), data['isPublic'])
        self.assertEqual(post.get('datePosted').strftime('%Y/%m/%d %H:%M:%S'),
                         data['datePosted'])

    def test_missing_title(self):
        """Test with missing title
        """
        response = self.client.post('/log', json={
            'content': 'Here is my post'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing title'})

    def test_missing_content(self):
        """Test with missing content
        """
        response = self.client.post('/log', json={
            'title': 'The Wonderful Tale'
        })
        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Missing content'})
