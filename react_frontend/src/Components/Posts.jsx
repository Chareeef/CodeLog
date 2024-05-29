

import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';

function Posts() {
  const [posts, setPosts] = useState([]);
  const [newPostText, setNewPostText] = useState('');
  const [comments, setComments] = useState({});
  const [newCommentText, setNewCommentText] = useState('');

  // Function to fetch posts from the backend API
  const fetchPosts = async () => {
    try {
      const response = await apiClient.get('/get_posts');
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  // Function to handle posting a new post
  const handlePostThought = async () => {
    try {
      const response = await apiClient.post('/post_thought', {
        body: newPostText,
      });
      console.log('New post posted:', response.data);
      // Fetch posts again to update the feed
      fetchPosts();
      // Clear the input field
      setNewPostText('');
    } catch (error) {
      console.error('Error posting thoughts today:', error);
    }
  };

  // Function to handle liking a post
  const handleLikePost = async (postId) => {
    try {
      const response = await apiClient.post('/like', {
        post_id: postId,
      });
      console.log('Post liked:', response.data);
      // Fetch posts again to update the feed
      fetchPosts();
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  // Function to handle posting a new comment
  const handlePostComment = async (postId) => {
    try {
      const response = await apiClient.post('/comment', {
        post_id: postId,
        body: newCommentText,
      });
      console.log('New comment posted:', response.data);
      // Fetch posts again to update the feed
      fetchPosts();
      // Clear the input field
      setNewCommentText('');
      // Update comments state
      setComments({
        ...comments,
        [postId]: comments[postId] ? [...comments[postId], response.data] : [response.data]
      });
    } catch (error) {
      console.error('Error posting comment:', error);
    }
  };

  // Function to handle deleting a comment
  const handleDeleteComment = async (postId, commentId) => {
    try {
      const response = await apiClient.delete('/delete_comment', {
        data: {
          post_id: postId,
          comment_id: commentId,
        },
      });
      console.log('Comment deleted:', response.data);
      // Fetch posts again to update the feed
      fetchPosts();
      // Remove the deleted comment from state
      setComments({
        ...comments,
        [postId]: comments[postId].filter(comment => comment._id !== commentId)
      });
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };

  // useEffect hook to fetch posts when the component mounts
  useEffect(() => {
    fetchPosts();
  }, []); // Empty dependency array ensures the effect runs only once on component mount

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-2xl font-bold mb-4">Feed 👨‍💻👩‍💻</h1>
      <h2 className="text-2xl font-bold mb-4">How was your Coding Journey today? Tell us all about it 🤗😊</h2>
      {/* Input field to post a new thought */}
      <div className="mb-4">
        <textarea
          className="w-full border border-gray-300 rounded p-2"
          rows="3"
          placeholder="What's on your mind?"
          value={newPostText}
          onChange={(e) => setNewPostText(e.target.value)}
        ></textarea>
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
          onClick={handlePostThought}
        >
          Post
        </button>
      </div>

      {/* Display posts */}
      <div>
        {posts.map((post) => (
          <div key={post._id} className="border border-gray-300 rounded p-4 mb-4">
            <p>{post.body}</p>
            <p className="text-sm text-gray-500">Posted by {post.user} on {new Date(post.datePosted).toLocaleString()}</p>

            {/* Like button */}
            <button
              className="bg-blue-500 text-white px-2 py-1 rounded mt-2 mr-2"
              onClick={() => handleLikePost(post._id)}
            >
              Like
            </button>
            
            {/* Comment input field */}
            <div className="mb-2">
              <textarea
                className="w-full border border-gray-300 rounded p-2"
                rows="2"
                placeholder="Leave a comment"
                value={newCommentText}
                onChange={(e) => setNewCommentText(e.target.value)}
              ></textarea>
              <button
                className="bg-gray-500 text-white px-2 py-1 rounded mt-2"
                onClick={() => handlePostComment(post._id)}
              >
                Comment
              </button>
            </div>
            
            {/* Display comments */}
            <div>
              {comments[post._id] && comments[post._id].map((comment) => (
                <div key={comment._id} className="border border-gray-300 rounded p-2 mb-2">
                  <p>{comment.body}</p>
                  <p className="text-xs text-gray-500">Posted by {comment.user} on {new Date(comment.datePosted).toLocaleString()}</p>
                  {/* Add delete comment button */}
                  <button
                    className="text-xs text-red-500 mt-1"
                    onClick={() => handleDeleteComment(post._id, comment._id)}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
            
          </div>
        ))}
      </div>
    </div>
  );
}

export default Posts;
