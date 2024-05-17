#!/usr/bin/env python3
"""The Home page routes
"""
from flask import Blueprint, jsonify, render_template, request
from datetime import datetime


# Create home Blueprint
home_bp = Blueprint('home_bp', __name__)

# NOTE: These routes will have @login_required when Auth is set

@home_bp.route('/')
def home():
    """Display the home page
    """
    return render_template('home.html')


@home_bp.route('/log', methods=['POST'])
def log():
    """Log a new entry
    """

    # Get data
    data = request.get_json()

    # Retrieve the entry's infos
    entry = {
        'title': data.get('title'),
        'content': data.get('content'),
        'date': datetime.utcnow(),
        'isPublic': data.get('isPublic', False)
    }

    # Store this log in MongoDB

    # Update user's current streak

    # Update user's longest streak if applicable

    # Reset user's current streak token in Redis for 28h

    # Recreate block entries token for this user in Redis for 20h

    # Return data
    return jsonify(entry)
