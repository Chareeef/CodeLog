#!/usr/bin/env python3
"""Set the app's configuration
"""
import os
import secrets
#from dotenv import load_dotenv
import datetime

# Load '.env' file
#load_dotenv()


class Config:
    """Configuration key-value pairs for our app
    """
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = os.getenv('FLASK_PORT', '5000')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)


class TestConfig(Config):
    """Testing configuration for our app
    """
    TESTING = True
