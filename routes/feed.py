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

    # If a page is queried, paginate with 20 posts per page
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

@feed_bp.route('/comment', methods=['POST'])
@jwt_required()
@verify_token_in_redis
def comment():
    """ route for adding comments to a post """
    # Get data from request
    data = request.get_json()

    # Get the post id
    post_id = data.get('post_id')

    # Get the current user's id
    user_id = get_jwt_identity()

    # comment body
    comment_body = data.get('body')

    # Check if post id is missing
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400

    # Return the post associated with post_id
    post = db.find_post({"_id": ObjectId(post_id)})

    # Check if the post exist.
    if post:
        comment_document = {
            'user_id': ObjectId(user_id),
            'post_id': ObjectId(post_id),
            'body': comment_body,
            'date_posted': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }

        comment_id = db.insert_comment(comment_document, post_id)
        comment = db.find_comment(comment_id, user_id)

        if comment_id:
            return jsonify(
                {
                'data': comment,
                "msg": "Comment created successfully."
                }
            ), 200

    return jsonify({"error": "Post not found."}), 404


@feed_bp.route('/update_comment', methods=['PUT'])
@jwt_required()
@verify_token_in_redis
def update_comment():
    """ route for updating comments from a post """
    # Get data from request
    data = request.get_json()

    # Get the post id
    post_id = data.get('post_id')

    # Get the current user's id
    user_id = get_jwt_identity()

    # comment id
    comment_id = data.get('comment_id')

    # Check if post id is missing
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400

    # Check if comment id is missing
    if not comment_id:
        return jsonify({"error": "Missing comment_id"}), 400

    # Get comment body
    comment_body = data.get('body')
    if not comment_body:
        return jsonify({"error": "Missing body"}), 400

    # Return the post associated with post_id
    post = db.find_post({"_id": ObjectId(post_id)})

    # Check if the post exist.
    if post:

        updated_comment = db.update_comment(comment_id, user_id, comment_body)
        if updated_comment:
            return jsonify(
                {
                    'data': updated_comment,
                    "msg": "Comment updated successfully."
                }
            ), 200

    return jsonify({"error": "Post not found."}), 404


@feed_bp.route('/delete_comment', methods=['DELETE'])
@jwt_required()
@verify_token_in_redis
def delete_comment():
    """ route for deleting comments from a post """
    # Get data from request
    data = request.get_json()

    # Get the post id
    post_id = data.get('post_id')

    # Get the current user's id
    user_id = get_jwt_identity()

    # comment id
    comment_id = data.get('comment_id')

    # Check if post id is missing
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400

    # Check if comment id is missing
    if not comment_id:
        return jsonify({"error": "Missing comment_id"}), 400


    # Return the post associated with post_id
    post = db.find_post({"_id": ObjectId(post_id)})

    # Check if the post exist.
    if post:

        deleted = db.delete_comment(comment_id, user_id, post_id)

        if deleted:
            return jsonify({"msg": "Comment deleted successfully."}), 200

    return jsonify({"error": "Post not found."}), 404

@feed_bp.route('/post_comments', methods=['GET'])
@jwt_required()
@verify_token_in_redis
def post_comments():
    """ route for returing all the comments associated with a post """
    # Get data from request
    data = request.get_json()

    # Get the post id
    post_id = data.get('post_id')

    # Check if post id is missing
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400

    # Return the post associated with post_id
    post = db.find_post({"_id": ObjectId(post_id)})

    # Check if the post exist.
    if post:

        # Get comments from db
        comments = db.get_post_comments(post_id)

        if comments:
            return jsonify(
                {
                    'data': comments,
                    "msg": "Comments retrieved successfully."
                }
            ), 200

    return jsonify({"error": "Post not found."}), 404
