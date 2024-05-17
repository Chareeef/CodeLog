#!/usr/bin/env python3
"""
Module for listing some stats about Nginx logs stored in MongoDB.
"""
from pymongo.errors import ConnectionFailure
from pymongo.results import InsertOneResult
from pymongo import MongoClient
from bson import ObjectId
import os
import bcrypt
from typing import Optional, Dict, Any, List


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
        document['password'] = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        )
        users = self._db['users']
        new_user = users.insert_one(document)
        return new_user

    def insert_post(self, document: Dict[str, Any]) -> InsertOneResult:
        """ Create a new post document """
        posts = self._db['posts']
        new_post = posts.insert_one(document)

        return new_post

    def find_user(self, **info: Dict[str, Any]) -> Optional[Dict[str, Any]]:

        """ Return a user document by email """
        users = self._db['users']
        try:
            user = users.find_one(info)
            return user
        except Exception as e:
            return None

    def find_user_posts(self, user_id: str) -> Optional[List[Dict[str, Any]]]:
        """ Return a posts documents created by a user. """
        posts = self._db['posts']
        try:
            user_posts = posts.find({'user_id': ObjectId(user_id)})
            return list(user_posts)
        except Exception as e:
            return None

    def find_all_users(self) -> List[Dict[str, Any]]:
        """ Returns all users in the db """
        users = self._db['users']
        return list(users.find())

    def find_all_posts(self) -> List[Dict[str, Any]]:
        """ Returns all posts in the db """
        posts = self._db['posts']
        return list(posts.find())
