#!/usr/bin/env python3
"""Initialize MongoDB client
"""
from db.db_manager import DBStorage
from db.redis_client import redis_client
import os

db = DBStorage()

if os.getenv('MODE') == 'TEST':
    db._db['posts'].delete_many({})
    db._db['users'].delete_many({})
