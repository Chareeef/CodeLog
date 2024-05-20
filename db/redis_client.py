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
redis_client = redis.Redis(host='localhost', port=6379, db=db_num)
print(f'Connected to Redis successfully on port: 6379, with db: {db_num}')
