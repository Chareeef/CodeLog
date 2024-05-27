#!/usr/bin/env python3
"""Create a Redis client
"""
import redis
import os


if os.getenv('MODE') == 'TEST':
    db_num = 1
else:
    db_num = 0

# Create Redis client
host = os.getenv('REDIS_HOST', '127.0.0.1')
redis_client = redis.Redis(host=host, port=6379, db=db_num)
print(f'Connected to Redis: host={host}, port=6379, db={db_num}')
