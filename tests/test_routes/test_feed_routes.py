#!/usr/bin/env python3
"""Module to test the Authentication route
"""
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from db.db_manager import check_hash_password
from main import create_app
import unittest


class FeedTests(unittest.TestCase):
    """ Tests for authenticated users """

    def setUp(self):
        """ Runs once before all tests """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        info = {
            'email': 'mohamed@example.com',
            'username': 'mohamed',
            'password': 'pass123',
            'current_streak': 0,
            'longest_streak': 0
        }
        self.user_id = db.insert_user(info)

        self.login_detail = {
            'email': 'mohamed@example.com',
            'password': 'pass123'
        }
        res = self.client.post('/login', json=self.login_detail)
        data = res.get_json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']

    def tearDown(self):
        """ Clear database """
        db.clear_db()
        rc.flushall()

