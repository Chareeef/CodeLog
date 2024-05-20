#!/usr/bin/env python3
"""The Home page routes
"""
from flask import Blueprint, jsonify, render_template, request
from datetime import datetime
from db import db

# Create home Blueprint
home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/log', methods=['POST'])
def log():
    """Log a new entry
    """

    # Get data
    data = request.get_json()

    # Retrieve the entry's infos
    entry = {
        'user_id': 'unujj',  # TODO: current_user.id
        'title': data.get('title'),
        'content': data.get('content'),
        'isPublic': data.get('isPublic', False),
        'datePosted': datetime.utcnow()
    }

    if not entry['title']:
        return jsonify({'error': 'Missing title'}), 400
    elif not entry['content']:
        return jsonify({'error': 'Missing content'}), 400

    # Store this log in MongoDB
    db.insert_post(entry)

    # Update user's current streak

    # Update user's longest streak if applicable

    # Reset user's current streak token in Redis for 28h

    # Recreate block entries token for this user in Redis for 20h

    # Return data
    entry['datePosted'] = entry['datePosted'].strftime('%Y/%m/%d %H:%M:%S')
    entry['_id'] = str(entry['_id'])
    return jsonify(entry), 201
