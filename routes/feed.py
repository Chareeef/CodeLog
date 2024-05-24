#!/usr/bin/env python3
""" Feed routes """
from flask import Blueprint, jsonify, request
from datetime import datetime
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import verify_token_in_redis
from bson import ObjectId

# Create feed Blueprint
feed_bp = Blueprint('feed_bp', __name__)


@feed_bp.route('/get_posts', methods=['GET'])
@jwt_required()
@verify_token_in_redis
def get_feed():
    """ Return all the public posts """
    posts = list(filter(lambda p: p['is_public'] == True, db.find_all_posts()))
    for p in posts:
        del p['_id']

    # Sort posts from the most to the less recent
    posts.sort(key=lambda x: x['datePosted'], reverse=True)

    # Stringify datePosted
    for p in posts:
        p['datePosted'] = p['datePosted'].strftime('%Y/%m/%d %H:%M:%S')

    # If a page is queried, paginante with 20 posts per page
    page = request.args.get('page')
    if page:
        try:
            page_num = int(page)

            if page_num < 1:
                return jsonify({'error': 'page number must be greater or equal to 1'}), 400

            # Compute posts quantity
            len_posts = len(posts)

            # Extract the page
            if (page_num - 1) * 20 > len_posts:
                return jsonify({'info': 'page out of range'})

            return jsonify(posts[(page_num - 1) * 20: page_num * 20])

        except ValueError:
            return jsonify({'error': 'page argument must be an integer'}), 400

    else:  # Return all posts with no pagination
        return jsonify(posts)


@feed_bp.route('/like', methods=['POST'])
@jwt_required()
@verify_token_in_redis
def like():
    """ Add likes to a post document """
    # Get data from request
    data = request.get_json()

    # Get the post id
    post_id = data.get('post_id')

    # Get the current user's id
    user_id = get_jwt_identity()

    # Check if post id is missing
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400

    # Return the post associated with post_id
    post = db.find_post({"_id": ObjectId(post_id)})

    # Check if the post exist.
    if post:

        # Check if the post is already liked by the current user
        liked = db.like_post(user_id, post['_id'])

        if liked:
            return jsonify({"error": "User has already liked the post."}), 400

        return jsonify({"success": "Post liked successfully."}), 200

    return jsonify({"error": "Post not found."}), 404


@feed_bp.route('/unlike', methods=['POST'])
@jwt_required()
@verify_token_in_redis
def unlike():
    """ remove likes from a post document """
    # Get data from request
    data = request.get_json()

    # Get the post id
    post_id = data.get('post_id')

    # Get the current user's id
    user_id = get_jwt_identity()

    # Check if post id is missing.
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400

    # Return the post associated with post_id
    post = db.find_post({"_id": ObjectId(post_id)})

    # Check if the post exist.
    if post:
        unliked = db.unlike_post(user_id, post['_id'])

        # Check if the post is already unliked by the current user
        if unliked:
            return jsonify(
                {"error": "User can only unliked the post that he liked."}
            ), 400

        return jsonify({"success": "Post unliked successfully."}), 200

    return jsonify({"error": "Post not found."}), 404
