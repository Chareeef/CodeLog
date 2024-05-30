import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';

function Posts() {
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState({});
  const [newCommentText, setNewCommentText] = useState('');

  // Function to fetch posts from the backend API
  const fetchPosts = async () => {
    try {
      const response = await apiClient.get('/feed/get_posts');
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  // Function to handle liking a post
  const handleLikePost = async (postId) => {
    try {
      const response = await apiClient.post('/feed/like', {
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
    console.log('postId'.postId);
    try {
      const response = await apiClient.post('/feed/comment', {
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
        [postId]: comments[postId]
          ? [...comments[postId], response.data]
          : [response.data],
      });
    } catch (error) {
      console.error('Error posting comment:', error);
    }
  };

  // Function to handle deleting a comment
  const handleDeleteComment = async (postId, commentId) => {
    try {
      const response = await apiClient.delete('/feed/delete_comment', {
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
        [postId]: comments[postId].filter(
          (comment) => comment._id !== commentId
        ),
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
    <div className='container mx-auto mt-8'>
      {/* Display posts */}
      <div>
        {posts.map((post) => (
          <div
            key={post._id}
            className='border border-gray-300 rounded p-4 mb-4'
          >
            <p>{post.title}</p>
            <p className='text-sm text-gray-500'>
              Posted by {post.username} on{' '}
              {new Date(post.datePosted).toLocaleString()}
            </p>
            <p>{post.content}</p>

            {/* Comment input field */}
            <div className='mb-2'>
              <textarea
                className='w-full border border-gray-300 rounded p-2'
                rows='2'
                placeholder='Leave a comment'
                value={newCommentText}
                onChange={(e) => setNewCommentText(e.target.value)}
              ></textarea>

              {/* Like button */}
              <button
                className='bg-blue-500 text-white px-2 py-1 rounded mt-2 mr-2'
                onClick={() => handleLikePost(post._id)}
              >
                Like
              </button>

              <button
                className='bg-gray-500 text-white px-2 py-1 rounded mt-2'
                onClick={() => handlePostComment(post._id)}
              >
                Comment
              </button>
            </div>

            {/* Display comments */}
            <div>
              {post.comment &&
                post.comments.map((comment) => (
                  <div
                    key={comment._id}
                    className='border border-gray-300 rounded p-2 mb-2'
                  >
                    <p>{comment.body}</p>
                    <p className='text-xs text-gray-500'>
                      Posted by {comment.user} on{' '}
                      {new Date(comment.datePosted).toLocaleString()}
                    </p>
                    {/* Add delete comment button */}
                    <button
                      className='text-xs text-red-500 mt-1'
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
