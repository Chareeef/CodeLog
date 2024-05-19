#!/usr/bin/env python3
"""The routes for the Authentication management
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
from db import db, redis_client as rc

# Create auth Blueprint
auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user
    """

    # Get data from request
    data = request.get_json()

    # Retrieve email
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    # Retrieve username
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Missing username'}), 400

    # Retrieve password
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Missing password'}), 400

    # Ensure email is not already used
    if db.find_user({'email': email}):
        return jsonify({'error': 'Email already used'}), 400

    # Ensure username is not already used
    if db.find_user({'username': username}):
        return jsonify({'error': 'Username already used'}), 400

    # Insert user to db
    doc = {
        'email': email,
        'username': username,
        'password': password
    }
    db.insert_user(doc)

    # Return respose
    return jsonify({'User created': username}), 201
