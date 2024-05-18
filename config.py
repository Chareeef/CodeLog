#!/usr/bin/env python3
"""Set the app's configuration
"""
import os
import secrets
from dotenv import load_dotenv

# Load '.env' file
load_dotenv()


class Config:
    """Configuration key-value pairs for our app
    """
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = os.getenv('FLASK_PORT', '5000')
