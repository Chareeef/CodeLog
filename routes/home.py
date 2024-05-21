#!/usr/bin/env python3
"""The Home page routes
"""
from bson import ObjectId
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import verify_token_in_redis
from db import db, redis_client as rc
from flask import Blueprint, jsonify, request
from routes.utils import get_user_id
import os

# Create home Blueprint
home_bp = Blueprint('home_bp', __name__)

# NOTE: These routes will maybe have @login_required when Auth is set


@home_bp.route('/')
@jwt_required()
@verify_token_in_redis
def home():
    """Display the home page
    """
    user = get_jwt_identity()
    if user:
        return jsonify({'success': f'logged in as {user}'}), 200

      
@home_bp.route('/log', methods=['POST'])
def log():
    """Log a new entry
    """

    # Get user_id
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 404

    # First, only allow one post in a 20h interval

    # Get the user
    user = db.find_user({'_id': ObjectId(user_id)})

    # Current streak key in Redis
    cs_key = f"{user['username']}_CS"

    # Define 20h as the minimum interval between two entries (0 < ttl < 8h)
    # or 2 seconds when testing
    if os.getenv('MODE') == 'TEST':
        max_allowed_ttl = 2
    else:
        max_allowed_ttl = 8 * 3600

    # Check current streak
    current_streak = rc.get(cs_key)
    if not current_streak:
        current_streak = 0
    elif rc.ttl(cs_key) > max_allowed_ttl:
        return jsonify({'error': 'Only one post per day is allowed'}), 400
    else:
        current_streak = int(current_streak.decode('utf-8'))

    # Get data
    data = request.get_json()

    # Retrieve the entry's infos
    entry = {
        'user_id': user_id,
        'title': data.get('title'),
        'content': data.get('content'),
        'is_public': data.get('is_public', False),
        'datePosted': datetime.utcnow()
    }

    if not entry['title']:
        return jsonify({'error': 'Missing title'}), 400
    elif not entry['content']:
        return jsonify({'error': 'Missing content'}), 400

    # Store this log in MongoDB
    db.insert_post(entry)

    # Make response
    response = entry.copy()
    response['_id'] = str(response['_id'])
    response['user_id'] = str(response['user_id'])

    time_fmt = '%Y/%m/%d %H:%M:%S'
    response['datePosted'] = response['datePosted'].strftime(time_fmt)

    # Response will return if the user marks a new longest streak
    response['new_record'] = False

    # Update user's current streak, and longest streak if applicable
    new_current_streak = current_streak + 1

    new_longest_streak = user['longest_streak']
    if new_current_streak > new_longest_streak:
        new_longest_streak = new_current_streak
        response['new_record'] = True

    db.update_user_info(user_id, {
        'current_streak': new_current_streak,
        'longest_streak': new_longest_streak
    })

    # Reset user's current streak key in Redis for 28h (4 seconds if testing)
    if os.getenv('MODE') == 'TEST':
        rc.setex(cs_key, 4, new_current_streak)
    else:
        rc.setex(cs_key, 28 * 3600, new_current_streak)

    # Return response
    return jsonify(response), 201
