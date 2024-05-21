#!/usr/bin/env python3
"""The routes for the Authentication management
"""
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from db import db, redis_client as rc
from functools import wraps
import bcrypt
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)


# Create auth Blueprint
auth_bp = Blueprint('auth_bp', __name__)


def store_token(token_key, token, ttl_seconds):
    """Store JWT in redis
    """
    rc.setex(token_key, ttl_seconds, token)


def is_token_expired(token_key):
    """Check if a JWT is stored and alive in Redis
    """
    return rc.exists(token_key)


def verify_token_in_redis(func):
    """Decorator to ensure a JWT presence
    """

    @wraps(func)
    def valid_token(*args, **kwargs):
        identity = get_jwt_identity()

        if not is_token_expired(identity):
            return jsonify({"error": "Token has been revoked"}), 401

        return func(*args, **kwargs)

    return valid_token


@auth_bp.route('/register', methods=['GET', 'POST'])
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
        'password': password,
        'created_at': datetime.utcnow(),
        'longest_streak': 0
    }
    db.insert_user(doc)

    # Return respose
    return jsonify({'Created user': username, 'email': email}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log in a user creating a JWT for him
    """
    login_details = request.get_json()

    # Verify that an email was sent
    email = login_details.get('email')
    if not email:
        return jsonify({'error': 'Missing email'}), 400

    # Verify that a password was sent
    password = login_details.get('password')
    if not password:
        return jsonify({'error': 'Missing password'}), 400

    # Get the user
    user_from_db = db.find_user({'email': email})

    if user_from_db:

        # Check that the password is correct
        hashed_password = db.get_hash(email)
        verified = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        if verified:

            # Create JWT Access Token
            access_token = create_access_token(
                identity=str(user_from_db['_id'])
            )

            # Create JWT Refresh Token
            refresh_token = create_refresh_token(
                identity=str(user_from_db['_id'])
            )

            # Store JWT Access Token
            store_token(
                str(user_from_db['_id']),
                access_token,
                current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            )

            # Store JWT Refresh Token
            store_token(
                str(user_from_db['_id']) + "_refresh",
                refresh_token,
                current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
            )

            # Return both JWTs as a response
            return jsonify(
                {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            ), 200

    # Return an error if credentials were wrong
    return jsonify({'error': 'The username or password is incorrect'}), 401


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh the current user's JWT
    """

    # Get the JWT identity of the current user
    current_user = get_jwt_identity()

    # Check JWT Refresh token
    key = current_user + '_refresh'
    if not is_token_expired(key):
        return jsonify({"error": "Token has been revoked"}), 401

    # Create and store a new JWT Access token
    new_access_token = create_access_token(identity=key)
    store_token(
        current_user,
        new_access_token,
        current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )

    # Return the new JWT Access Token
    return jsonify({'new_access_token': new_access_token}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@verify_token_in_redis
def logout():
    """Invalidate JWTs by deleting them from Redis
    """
    current_user = get_jwt_identity()
    rc.delete(current_user)
    rc.delete(current_user + "_refresh")

    return jsonify({}), 204
