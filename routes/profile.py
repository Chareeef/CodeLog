#!/usr/bin/env python3
"""The routes for the user space management
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
from db import db, redis_client as rc

# Create profile Blueprint
profile_bp = Blueprint('profile_bp', __name__)

# NOTE: These routes will maybe have @login_required when Auth is set


@profile_bp.route('/posts')
def get_posts():
    """Get the user's posts
    """

    # Search Authentication token in Redis, and get userId
    auth_token = request.headers.get('x-token')
    userId = rc.get(auth_token)
    if not userId:
        return jsonify({'error': 'Unauthorized'}), 404

    # Return posts
    posts = db.find_user_posts(userId.decode('utf-8'))
    for p in posts:
        del p['_id']
        del p['userId']
        p['datePosted'] = p['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    return jsonify(posts)
