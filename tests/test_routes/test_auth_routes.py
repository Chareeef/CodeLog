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
            'current_streak': 0,
            'longest_streak': 0
        }
        db.insert_user(infos)

    @classmethod
    def tearDownClass(cls):
        """Clear database
        """
        db._db['users'].delete_many({})

    def test_register_success(self):
        """Test successefully registering a user
        """
        infos = {
            'email': 'leviosa@poud.com',
            'username': 'minervahog67',
            'password': 'mcgonacat',
        }
        response = self.client.post('/register', json=infos)

        self.assertEqual(response.status_code, 201)

        # Check stored user
        user = db.find_user({'email': infos['email']})

        self.assertEqual(user.get('email'), infos['email'])
        self.assertEqual(user.get('username'), infos['username'])
        self.assertEqual(user.get('current_streak'), 0)
        self.assertEqual(user.get('longest_streak'), 0)
        self.assertEqual(user.get('created_at').strftime('%Y/%m/%d %H:%M:%S'),
                         datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))

        hashed_pwd = db.get_hash(infos['email'])
        self.assertTrue(check_hash_password(infos['password'], hashed_pwd))
