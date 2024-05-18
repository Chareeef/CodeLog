#!/usr/bin/env python3
"""The routes for the user space management
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
from db import db

# Create profile Blueprint
profile_bp = Blueprint('profile_bp', __name__)

# NOTE: These routes will have @login_required when Auth is set


@profile_bp.route('/posts', methods=['POST'])
def get_posts():
    """Get the user's posts
    """
    userId = request.get_json().get('userId')
    if not db.find_user(userId):
        return jsonify({'error': 'Unauthorized'}), 404

    return db.find_user_posts(userId)
