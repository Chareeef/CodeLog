#!/usr/bin/env python3
"""
Module for managing storage of SWE_journal in MongoDB.
"""
from pymongo.errors import ConnectionFailure
from pymongo import ReturnDocument
from pymongo.results import InsertOneResult
from pymongo import MongoClient
from bson import ObjectId
import os
import bcrypt
from typing import Any, Dict, List, Optional, Union


def hash_pass(password: str) -> bytes:
    """ hashs a password and return the hashed value """
    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hash_password


def check_hash_password(hashed_password: str, password: str) -> bool:
    """ check if hashed value of two string are the same """
    hash_password = hash_pass(password)
    is_ok = bcrypt.checkpw(hashed_password, hash_password)

    return is_ok


class DBStorage:
    """ Defines a class that manages storage of SWE_journal in MongoDB. """

    def __init__(self) -> None:
        """ Constructor """
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '27017')
        db_name = os.getenv('DB_DATABASE', 'swe_journal')
        self._client = MongoClient(f"mongodb://{db_host}:{db_port}/")

        try:
            self._client.admin.command('ismaster')
            print(f"Connected to MongoDB successfully on port: {db_port}")
        except ConnectionFailure as err:
            print(f"Connection failed: {err}")
            raise

        self._db = self._client[db_name]

    def insert_user(self, document: Dict[str, Any]) -> InsertOneResult:
        """ Create a new user document """
        password = document['password']
        document['password'] = hash_pass(password)
        users = self._db['users']
        new_user = users.insert_one(document)
        return new_user

    def insert_post(self, document: Dict[str, Any]) -> InsertOneResult:
        """ Create a new post document """
        posts = self._db['posts']
        new_post = posts.insert_one(document)

        return new_post

    def find_user(self, info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """ Return a user document """
        users = self._db['users']
        try:
            user = users.find_one(info)
            user.pop('password', None)
            return user
        except Exception as e:
            return None

    def find_post(self, info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """ Return a post document """
        posts = self._db['posts']
        try:
            post = posts.find_one(info)
            return post
        except Exception as e:
            return None

    def find_user_posts(self, userId: str) -> Optional[List[Dict[str, Any]]]:
        """ Return a posts documents created by a user """
        posts = self._db['posts']
        try:
            user_posts = posts.find({'userId': ObjectId(userId)})
            return list(user_posts)
        except Exception as e:
            print(e)
            return None

    def update_user_info(
            self,
            userId: str,
            update_fields: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """ update and return a user document. """
        users = self._db['users']
        update_fields.pop('password', None)
        try:
            updated_user = users.find_one_and_update(
                {'_id': ObjectId(userId)},
                {'$set': update_fields},
                return_document=ReturnDocument.AFTER
            )
            return updated_user
        except Exception as e:
            return None

    def update_user_password(
            self,
            userId: str,
            new_password: str,
            old_password: str
    ) -> Union[ObjectId, None]:
        """ Update the user's password as hash """
        users = self._db['users']
        user = users.find_one({'_id': ObjectId(userId)})

        if not user:
            return None

        if not check_hash_password(user['password'], old_password):
            return None

        new_hashed_password = hash_pass(new_password)
        try:
            users.find_one_and_update(
                {'_id': ObjectId(userId)},
                {'$set': {'password': new_hashed_password}}
            )
            return userId
        except Exception as e:
            return None

    def update_post(
            self,
            postId: str,
            userId: str,
            update_fields: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """ update and return a post document. """
        posts = self._db['posts']
        try:
            updated_post = posts.find_one_and_update(
                {'_id': ObjectId(postId), 'userId': ObjectId(userId)},
                {'$set': update_fields},
                return_document=ReturnDocument.AFTER
            )
            return updated_post
        except Exception as e:
            return None

    def delete_post(self, postId: str, userId: str) -> bool:
        """ deletes a post ducoment from db """
        posts = self._db['posts']
        try:
            posts.delete_one({
                '_id': ObjectId(postId),
                'userId': ObjectId(userId)
            })
            return True
        except Exception as e:
            return False

    def find_all_users(self) -> List[Dict[str, Any]]:
        """ Returns all users in the db """
        users = self._db['users']
        return list(users.find())

    def find_all_posts(self) -> List[Dict[str, Any]]:
        """ Returns all posts in the db """
        posts = self._db['posts']
        return list(posts.find())
