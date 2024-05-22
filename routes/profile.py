#!/usr/bin/env python3
"""The routes for the user space management
"""
from bson import ObjectId
from flask import Blueprint, jsonify, request
from datetime import datetime
from db import db, redis_client as rc
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import verify_token_in_redis

# Create profile Blueprint
profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/get_infos')
@jwt_required()
@verify_token_in_redis
def get_infos():
    """Get user's email and username
    """

    # Get the user
    user_id = get_jwt_identity()
    user = db.find_user({'_id': ObjectId(user_id)})

    # Return response
    response = {'email': user['email'], 'username': user['username']}
    return jsonify(response)


@profile_bp.route('/streaks')
@jwt_required()
@verify_token_in_redis
def get_streaks():
    """Get user's current and longest streaks
    """

    # Get the user
    user_id = get_jwt_identity()
    user = db.find_user({'_id': ObjectId(user_id)})

    # Get longest streak
    longest_streak = user['longest_streak']

    # Get current streak
    cs_key = user['username'] + '_CS'
    current_streak = rc.get(cs_key)
    if not current_streak:
        current_streak = 0
    else:
        current_streak = int(current_streak.decode('utf-8'))

    # Return response
    response = {'longest_streak': longest_streak,
                'current_streak': current_streak}
    return jsonify(response)


@profile_bp.route('/posts')
@jwt_required()
@verify_token_in_redis
def get_posts():
    """Get the user's posts
    """

    # Get the user_id
    user_id = get_jwt_identity()

    # Return posts
    posts = db.find_user_posts(user_id)
    for p in posts:
        del p['_id']
        del p['user_id']
        p['datePosted'] = p['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    return jsonify(posts)


@profile_bp.route('/update_infos', methods=['PUT'])
@jwt_required()
@verify_token_in_redis
def update_infos():
    """Update the user's infos
    """

    # Get the user_id
    user_id = get_jwt_identity()

    # Get the data to update
    data = request.get_json()

    # Check fields
    accepted_fields = ['email', 'username']
    for field in data.keys():
        if field not in accepted_fields:
            return jsonify({'error': 'Only update email and/or username'}), 400

    # Update the user's infos
    db.update_user_info(user_id, data)

    return jsonify({'success': 'user updated'}), 201


@profile_bp.route('/update_password', methods=['PUT'])
@jwt_required()
@verify_token_in_redis
def update_password():
    """Update the user's password
    """

    # Get the user_id
    user_id = get_jwt_identity()

    # Get the new and old password
    data = request.get_json()

    # Check fields
    old_pwd = data.get('old_password')
    if not old_pwd:
        return jsonify({'error': 'Missing old password'}), 400

    new_pwd = data.get('new_password')
    if not new_pwd:
        return jsonify({'error': 'Missing new password'}), 400

    # Try to update password
    response = db.update_user_password(user_id, old_pwd, new_pwd)

    # Return response
    return jsonify(response[0]), response[1]
