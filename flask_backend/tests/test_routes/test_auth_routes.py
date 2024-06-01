#!/usr/bin/env python3
"""Module to test the Authentication route
"""
from config import TestConfig
from datetime import datetime
from db import db, redis_client as rc
from db.db_manager import check_hash_password
from main import create_app
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
        response = self.client.post('/api/register', json=infos)

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
        self.assertAlmostEqual(user.get('created_at').strftime(time_fmt),
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
        response = self.client.post('/api/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Missing email'})

    def test_register_with_missing_username(self):
        """Test registering a user with missing username
        """
        infos = {
            'email': 'leviosa@poud.com',
            'password': 'mcgonacat',
        }
        response = self.client.post('/api/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Missing username'})

    def test_register_with_missing_password(self):
        """Test registering a user with missing password
        """
        infos = {
            'email': 'leviosa@poud.com',
            'username': 'minervahog67'
        }
        response = self.client.post('/api/register', json=infos)

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
        response = self.client.post('/api/register', json=infos)

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
        response = self.client.post('/api/register', json=infos)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {
                         'error': 'Username already used'})


class LoginTests(unittest.TestCase):
    """ Tests for Login route """

    def setUp(self):
        """Runs once before all tests
        """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        info = {
            'email': 'mohamed@example.com',
            'username': 'mohamed',
            'password': 'pass123',
            'current_streak': 0,
            'longest_streak': 0
        }
        db.insert_user(info)

        self.login_detail = {
            'email': 'mohamed@example.com',
            'password': 'pass123'
        }

    def tearDown(cls):
        """Clear database
        """
        db.clear_db()

    def test_login_success(self):
        """ Test logging a user successfully  """

        res = self.client.post('/api/login', json=self.login_detail)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)

    def test_login_with_bad_email(self):
        """ Test logging a user with incorrect email  """
        login_detail = {
            'email': 'bad@email.com',
            'password': 'pass123'
        }

        res = self.client.post('/api/login', json=login_detail)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            data, {'error': 'The email and/or password are incorrect'}
        )
        self.assertNotIn('access_token', data)
        self.assertNotIn('refresh_token', data)

    def test_login_with_bad_password(self):
        """ Test logging a user with incorrect password  """
        login_detail = {
            'email': 'mohamed@example.com',
            'password': 'badpass'
        }

        res = self.client.post('/api/login', json=login_detail)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            data, {'error': 'The email and/or password are incorrect'}
        )
        self.assertNotIn('access_token', data)
        self.assertNotIn('refresh_token', data)

    def test_login_with_missing_password(self):
        """ Test logging a user with missing password  """
        login_detail = {
            'email': 'mohamed@example.com',
        }

        res = self.client.post('/api/login', json=login_detail)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, {'error': 'Missing password'})
        self.assertNotIn('access_token', data)
        self.assertNotIn('refresh_token', data)

    def test_login_with_missing_email(self):
        """ Test logging a user with missing email  """
        login_detail = {
            'password': 'pass123',
        }

        res = self.client.post('/api/login', json=login_detail)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, {'error': 'Missing email'})
        self.assertNotIn('access_token', data)
        self.assertNotIn('refresh_token', data)


class LoggedInTests(unittest.TestCase):
    """ Tests for authenticated users """

    def setUp(self):
        """Runs once before all tests
        """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        info = {
            'email': 'mohamed@example.com',
            'username': 'mohamed',
            'password': 'pass123',
            'current_streak': 0,
            'longest_streak': 0
        }
        self.username = info['username']
        self.user_id = db.insert_user(info)

        self.login_detail = {
            'email': 'mohamed@example.com',
            'password': 'pass123'
        }
        res = self.client.post('/api/login', json=self.login_detail)
        data = res.get_json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']

    def tearDown(self):
        """Clear database
        """
        db.clear_db()
        rc.flushall()

    def test_access_protected_route_success(self):
        """ Test a logged in user has access to protected routes """
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        res = self.client.get('/api/', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, {'user_id': str(
            self.user_id), 'username': self.username})

    def test_access_protected_route_with_bad_token(self):
        """ Test a logged in user has access
        to protected routes witha bad token """
        headers = {
            'Authorization': 'Bearer badtoken'
        }
        res = self.client.get('/api/', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'}
        )

    def test_access_protected_route_with_no_token(self):
        """ Test a logged in user has access
        to protected routes witha bad token """
        res = self.client.get('/api/')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})

    def test_access_protected_route_with_expired_token(self):
        """ Test a logged in user has access to
        protected routes witha bad token """
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        rc.delete(str(self.user_id))

        res = self.client.get('/api/', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Token has been revoked'})

    def test_get_new_access_token_success(self):
        """ Test get a new access token """
        headers = {
            'Authorization': f'Bearer {self.refresh_token}'
        }
        res = self.client.post('/api/refresh', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertIn('new_access_token', data)

        headers = {
            "Authorization": f"Bearer {data['new_access_token']}"
        }

        res = self.client.get('/api/', headers=headers)

        self.assertEqual(res.status_code, 200)

    def test_get_new_access_token_fail(self):
        """ Test get new access token with a bad refresh token. """
        headers = {
            'Authorization': f'Bearer badrefreshtoken'
        }

        res = self.client.post('/api/refresh', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            data, {'error': 'The token is invalid or has expired'}
        )
        self.assertNotIn('new_access_token', data)

    def test_get_new_access_token_fail_too(self):
        """ Test get new access token with an expired refresh token. """
        headers = {
            'Authorization': f'Bearer {self.refresh_token}'
        }
        rc.delete(str(self.user_id) + '_refresh')

        res = self.client.post('/api/refresh', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Token has been revoked'})
        self.assertNotIn('new_access_token', data)

    def test_get_new_access_token_fail_three(self):
        """ Test get new access token with an no refresh token. """

        res = self.client.post('/api/refresh')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})
        self.assertNotIn('new_access_token', data)

    def test_logout(self):
        """ Test logout users successfully """
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        res = self.client.post('/api/logout', headers=headers)

        self.assertEqual(res.status_code, 204)
        self.assertIsNone(rc.get(str(self.user_id)))

    def test_logout_missing_token(self):
        """ Test logout users with a missing authorization header """
        res = self.client.post('/api/logout')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Missing Authorization Header'})
        self.assertIsNotNone(rc.get(str(self.user_id)))

    def test_logout_expired_token(self):
        """ Test logout with an expired access token """
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        rc.delete(str(self.user_id))

        res = self.client.post('/api/logout', headers=headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data, {'error': 'Token has been revoked'})
