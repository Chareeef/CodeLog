#!/usr/bin/env python3
"""Helper functions for routes
"""
from flask import request
from typing import Optional
from db import redis_client as rc


def get_user_id() -> Optional[str]:
    """Get the user's id with authentictation token
    """

    # Search Authentication token in Redis, and get user_id
    auth_token = request.headers.get('x-token')
    user_id = rc.get(auth_token)

    if user_id:
        return user_id.decode('utf-8')
    else:
        return None
