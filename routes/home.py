#!/usr/bin/env python3
"""The Home page routes
"""
from bson import ObjectId
from datetime import datetime
from db import db, redis_client as rc
from flask import Blueprint, jsonify, request
from routes.utils import get_user_id

# Create home Blueprint
home_bp = Blueprint('home_bp', __name__)


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

    # Check current streak
    cs_key = f"{user['username']}_CS"  # current streak key in Redis
    current_streak = rc.get(cs_key)
    if not current_streak:
        current_streak = 0
    elif rc.ttl(cs_key) > 8 * 3600:
        return jsonify({'error': 'Only one post per day is allowed'}), 400

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
        'longest_streak': new_current_streak
    })

    # Reset user's current streak token in Redis for 28h
    rc.setex(cs_key, 28 * 3600, new_current_streak)

    # Return response
    return jsonify(response), 201
