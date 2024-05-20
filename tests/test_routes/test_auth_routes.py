#!/usr/bin/env python3
"""Module to test the Authentication route
"""
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from db.db_manager import check_hash_password
from main import create_app
import string
import random
import unittest


class TestRegister(unittest.TestCase):
    """Tests for 'POST /register' route
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
            'email': 'lumos@poud.com',
            'username': 'albushog99',
            'password': 'gumbledore',
            'longest_streak': 0
        }
        db.insert_user(infos)

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db.clear_db()

    def test_register_success(self):
        """Test successefully registering a user
        """
        infos = {
            'email': 'leviosa@poud.com',
            'username': 'minervahog67',
            'password': 'mcgonacat'
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(),
                         {
                             'Created user': infos['username'],
                             'email': infos['email']
        })

        # Check stored user
        user = db.find_user({'email': infos['email']})

        self.assertEqual(user.get('email'), infos['email'])
        self.assertEqual(user.get('username'), infos['username'])
        self.assertEqual(user.get('longest_streak'), 0)

        time_fmt = '%Y/%m/%d %H:%M:%S'
        self.assertEqual(user.get('created_at').strftime(time_fmt),
                         datetime.utcnow().strftime(time_fmt))

        hashed_pwd = db.get_hash(infos['email'])
        self.assertTrue(check_hash_password(hashed_pwd, infos['password']))

    def test_register_with_missing_email(self):
        """Test registering a user with missing email
        """
        infos = {
            'username': 'minervahog67',
            'password': 'mcgonacat'
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Missing email'})

    def test_register_with_missing_username(self):
        """Test registering a user with missing username
        """
        infos = {
            'email': 'leviosa@poud.com',
            'password': 'mcgonacat',
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Missing username'})

    def test_register_with_missing_password(self):
        """Test registering a user with missing password
        """
        infos = {
            'email': 'leviosa@poud.com',
            'username': 'minervahog67'
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Missing password'})

    def test_register_with_used_email(self):
        """Test registering a user with already used email
        """
        infos = {
            'email': 'lumos@poud.com',
            'username': 'podalbus89',
            'password': 'hog478',
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Email already used'})

    def test_register_with_used_username(self):
        """Test registering a user with already used username
        """
        infos = {
            'email': 'revelio@poud.com',
            'username': 'albushog99',
            'password': 'hog478',
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {
                         'error': 'Username already used'})
