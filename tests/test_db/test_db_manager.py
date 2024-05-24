#!/usr/bin/env python3
"""
Module unittest for the db_manager.
"""
import unittest
from unittest.mock import patch
import mongomock
from db import db
from bson import ObjectId
from datetime import datetime


class TestDBStorage(unittest.TestCase):
    """ Defines a class for testing DBStorage. """

    @patch('db.db_manager.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        """Set up a mock MongoDB client before each test."""
        self.db = db

    def tearDown(self):
        """ Clean up the database after each test """
        self.db.clear_db()

    def test_insert_and_find_user(self):
        """Test inserting and finding a user document."""
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0

        }
        inserted_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_id, ObjectId)
        inserted_doc = self.db.find_user({'_id': inserted_id})

        self.assertIsNotNone(inserted_doc)

        self.assertEqual(inserted_doc['username'], 'Mohamed')
        self.assertEqual(inserted_doc['email'], 'mohamed@example.com')
        self.assertEqual(inserted_doc['longest_streak'], 0)

        self.assertFalse('password' in inserted_doc)

    def test_update_user_info(self):
        """ Test updating user's info. """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0
        }
        updated_info = {
            'username': 'Mohamed123',
            'longest_streak': 2
        }
        inserted_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_id, ObjectId)

        self.db.update_user_info(inserted_id, updated_info)
        inserted_doc = self.db.find_user({'_id': inserted_id})

        self.assertEqual(inserted_doc['email'], 'mohamed@example.com')
        self.assertEqual(inserted_doc['longest_streak'], 2)

    def test_update_user_password(self):
        """ Test updating user's password. """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'oldpassword',
            'longest_streak': 0
        }
        inserted_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_id, ObjectId)

        result = self.db.update_user_password(
            inserted_id,
            'oldpassword',
            'newpassword'
        )
        self.assertEqual(result, 0)

    def test_update_user_with_wrong_password(self):
        """ Test updating user's password. """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'oldpassword',
            'longest_streak': 0
        }
        inserted_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_id, ObjectId)

        result = self.db.update_user_password(
            inserted_id,
            'wrongpassword',
            'newpassword'
        )
        self.assertEqual(result, -2)

    def test_insert_and_find_post(self):
        """ Test create and find post """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0
        }
        inserted_user_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_user_id, ObjectId)

        post_document = {
            'user_id': inserted_user_id,
            'title': 'Post\'s title',
            'content': 'Post\'s content',
            'is_public': False,
            'date_posted': datetime.utcnow()
        }
        inserted_post_id = self.db.insert_post(post_document)
        self.assertIsInstance(inserted_post_id, ObjectId)

        post = self.db.find_post(
            {
                '_id': inserted_post_id,
                'user_id': inserted_user_id
            }
        )
        self.assertEqual(post['title'], post_document['title'])
        self.assertEqual(post['is_public'], post_document['is_public'])
        self.assertEqual(post['user_id'], str(inserted_user_id))

    def test_update_post(self):
        """ Test update a new post """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0
        }
        inserted_user_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_user_id, ObjectId)

        post_document = {
            'user_id': inserted_user_id,
            'title': 'Post\'s title',
            'content': 'Post\'s content',
            'is_public': False,
            'date_posted': datetime.utcnow()
        }
        inserted_post_id = self.db.insert_post(post_document)
        self.assertIsInstance(inserted_post_id, ObjectId)
        update_post = {
            'title': 'New title',
            'content': 'New content',
            'is_public': True
        }
        self.db.update_post(
            inserted_post_id,
            inserted_user_id,
            update_post
        )

        post = self.db.find_post(
            {
                '_id': inserted_post_id,
                'user_id': inserted_user_id
            }
        )
        self.assertEqual(post['title'], update_post['title'])
        self.assertEqual(post['is_public'], update_post['is_public'])

    def test_delete_post(self):
        """ Test delete a post """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0
        }
        inserted_user_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_user_id, ObjectId)

        post_document = {
            'user_id': inserted_user_id,
            'title': 'Post\'s title',
            'content': 'Post\'s content',
            'is_public': False,
            'date_posted': datetime.utcnow()
        }
        inserted_post_id = self.db.insert_post(post_document)
        self.assertIsInstance(inserted_post_id, ObjectId)
        deleted = self.db.delete_post(
            inserted_post_id,
            inserted_user_id
        )

        post = self.db.find_post(
            {
                '_id': inserted_post_id,
                'user_id': inserted_user_id
            }
        )
        self.assertTrue(deleted)
        self.assertIsNone(post)

    def test_get_user_posts(self):
        """ Test to get all of the user's posts """
        user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0
        }
        inserted_user_id = self.db.insert_user(user_document)
        self.assertIsInstance(inserted_user_id, ObjectId)

        post_document_1 = {
            'user_id': inserted_user_id,
            'title': 'Post 1 title',
            'content': 'Post 1 content',
            'is_public': False,
            'date_posted': datetime.utcnow()
        }
        post_document_2 = {
            'user_id': inserted_user_id,
            'title': 'Post 2 title',
            'content': 'Post 2 content',
            'is_public': False,
            'date_posted': datetime.utcnow()
        }
        post_document_3 = {
            'user_id': ObjectId(),
            'title': 'Post 2 title',
            'content': 'Post 2 content',
            'is_public': False,
            'date_posted': datetime.utcnow()
        }
        inserted_post1_id = self.db.insert_post(post_document_1)
        inserted_post2_id = self.db.insert_post(post_document_2)
        inserted_post2_id = self.db.insert_post(post_document_3)

        self.assertIsInstance(inserted_post1_id, ObjectId)
        self.assertIsInstance(inserted_post2_id, ObjectId)

        posts = self.db.find_user_posts(inserted_user_id)

        self.assertEqual(len(posts), 2)
        self.assertEqual(len(self.db.find_all_posts()), 3)
        self.assertEqual(posts[0]['user_id'], str(inserted_user_id))
        self.assertEqual(posts[1]['user_id'], str(inserted_user_id))


class TestComment(unittest.TestCase):
    """ Tests for the comment document """
    @patch('db.db_manager.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        """Set up a mock MongoDB client before each test."""
        self.db = db

        self.user_document = {
            'username': 'Mohamed',
            'email': 'mohamed@example.com',
            'password': 'password123',
            'longest_streak': 0

        }
        self.inserted_user_id = self.db.insert_user(self.user_document)

        self.second_user_document = {
            'username': 'Youssef',
            'email': 'youssef@example.com',
            'password': 'password123',
            'longest_streak': 0

        }
        self.inserted_second_user_id = self.db.insert_user(
            self.second_user_document
        )

        self.post_document = {
            'user_id': self.inserted_user_id,
            'title': 'Post title',
            'content': 'Post content',
            'likes': [],
            'number_of_likes': 0,
            'comments': [],
            'number_of_comments': 0,
        }
        self.inserted_post_id = self.db.insert_post(self.post_document)

    def tearDown(self):
        """ Clean up the database after each test """
        self.db.clear_db()

    def test_add_comment_to_post(self):
        """ Test create a new comment """
        comment_document = {
            'user_id': self.inserted_user_id,
            'body': 'First comment',
            'post_id': self.inserted_post_id

        }
        comment_id = self.db.insert_comment(
            comment_document, self.inserted_post_id
        )

        self.assertIsInstance(comment_id, ObjectId)

        post = self.db.find_post({'_id': self.inserted_post_id})

        self.assertEqual(post['number_of_comments'], 1)
        self.assertIn(comment_id, post['comments'])

    def test_find_comment(self):
        """ Test create a new comment """
        comment_document = {
            'user_id': self.inserted_user_id,
            'body': 'First comment',
            'post_id': self.inserted_post_id
        }
        comment_id = self.db.insert_comment(
            comment_document, self.inserted_post_id
        )

        self.assertIsInstance(comment_id, ObjectId)

        post = self.db.find_post({'_id': self.inserted_post_id})

        self.assertEqual(post['number_of_comments'], 1)
        self.assertIn(comment_id, post['comments'])

        comment = self.db.find_comment(comment_id, self.inserted_user_id)

        self.assertEqual(
            ObjectId(comment['user_id']), comment_document['user_id']
        )
        self.assertEqual(comment['body'], comment_document['body'])

    def test_update_comment(self):
        """ Test updating a comment documment """
        comment_document = {
            'user_id': self.inserted_user_id,
            'body': 'Second comment',
            'post_id': self.inserted_post_id
        }
        comment_id = self.db.insert_comment(
            comment_document, self.inserted_post_id
        )

        self.assertIsInstance(comment_id, ObjectId)

        post = self.db.find_post({'_id': self.inserted_post_id})
        comment = self.db.find_comment(comment_id, self.inserted_user_id)

        self.assertEqual(comment['body'], comment_document['body'])
        self.assertEqual(post['number_of_comments'], 1)
        self.assertIn(comment_id, post['comments'])
        body = {
            'body': 'Updated comment'
        }

        updated_comment = self.db.update_comment(
            comment_id, self.inserted_user_id, body
        )

        comment = self.db.find_comment(comment_id, self.inserted_user_id)

        self.assertEqual(comment['body'], updated_comment['body'])
        self.assertEqual(post['number_of_comments'], 1)
        self.assertIn(comment_id, post['comments'])

    def test_delete_comment(self):
        """ Test deleting a comment documment """
        comment_document = {
            'user_id': self.inserted_user_id,
            'body': 'Second comment',
            'post_id': self.inserted_post_id
        }
        comment_id = self.db.insert_comment(
            comment_document, self.inserted_post_id
        )

        self.assertIsInstance(comment_id, ObjectId)

        post = self.db.find_post({'_id': self.inserted_post_id})
        comment = self.db.find_comment(comment_id, self.inserted_user_id)

        self.assertEqual(comment['body'], comment_document['body'])
        self.assertEqual(post['number_of_comments'], 1)
        self.assertIn(comment_id, post['comments'])

        deleted = self.db.delete_comment(
            comment_id, self.inserted_user_id, self.inserted_post_id
        )

        self.assertTrue(deleted)

        post = self.db.find_post({'_id': self.inserted_post_id})
        comment = self.db.find_comment(comment_id, self.inserted_user_id)

        self.assertIsNone(comment)
        self.assertEqual(post['number_of_comments'], 0)
        self.assertNotIn(comment_id, post['comments'])

    def test_get_post_comments(self):
        """ Test to return all comments associated with a post """
        comment_document_1 = {
            'user_id': self.inserted_user_id,
            'body': 'Second comment',
            'post_id': self.inserted_post_id

        }
        comment_document_2 = {
            'user_id': self.inserted_second_user_id,
            'body': 'Second comment',
            'post_id': self.inserted_post_id
        }
        comment_id_1 = self.db.insert_comment(
            comment_document_1, self.inserted_post_id
        )
        comment_id_2 = self.db.insert_comment(
            comment_document_2, self.inserted_post_id
        )

        self.assertIsInstance(comment_id_1, ObjectId)
        self.assertIsInstance(comment_id_2, ObjectId)

        post = self.db.find_post({'_id': self.inserted_post_id})

        self.assertEqual(post['number_of_comments'], 2)
        self.assertIn(comment_id_1, post['comments'])
        self.assertIn(comment_id_2, post['comments'])

        comments = self.db.get_post_comments(post['_id'])

        self.assertEqual(len(comments), 2)

    def test_delete_comments_post(self):
        """ Test for removing all comments associated with a post
        when the post is deleted"""
        pass

    def test_delete_comments_user(self):
        """ Test for removing all comments associated with a post
        when the user is deleted"""
        pass


if __name__ == '__main__':
    unittest.main()
