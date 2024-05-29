#!/usr/bin/env python3
"""Initialize MongoDB client
"""
from db.db_manager import DBStorage
from db.redis_client import redis_client

db = DBStorage()
