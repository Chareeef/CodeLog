import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import nl2br from 'react-nl2br';

import apiClient from '../apiClient';
import Footer from './Footer';

function Posts() {
  const [username, setUsername] = useState('');
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState({});
  const [showComments, setShowComments] = useState(false);
  const [newCommentText, setNewCommentText] = useState('');
  const navigate = useNavigate();

  const check_auth = async () => {
    try {
      const res = await apiClient.get('/');
      setUsername(res.data.username);
      console.log(res);
      console.log(username);
    } catch (error) {
      console.error(error);
      alert(
        'Sorry, it seems your Authentication was lost or corrupted. Please log in again.'
      );
      localStorage.removeItem('jwt_access_token');
      localStorage.removeItem('jwt_refresh_token');
      navigate('/login');
    }
  };

  // Function to fetch posts from the backend API
  const fetchPosts = async () => {
    try {
      const res = await apiClient.get('/feed/get_posts');
      const posts = res.data;
      setPosts(posts);
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

  // Function to handle unliking a post
  const handleUnlikePost = async (postId) => {
    try {
      const response = await apiClient.post('/feed/unlike', {
        post_id: postId,
      });
      console.log('Post unliked:', response.data);
      // Fetch posts again to update the feed
      fetchPosts();
    } catch (error) {
      console.error('Error unliking post:', error);
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
    check_auth();
    fetchPosts();
  }, []); // Empty dependency array ensures the effect runs only once on component mount

  return (
    <div className='d-flex flex-column min-vh-100'>
      {/* Display posts */}
      <div className='bg-beige flex-1 flex-grow-1 d-flex flex-column justify-content-center p-3'>
        {posts.map((post) => (
          <div
            key={post._id}
            className='card m-2 border border-gray-300 rounded p-4'
          >
            <div className='card-body'>
              <div className='border-orange rounded p-2 mb-2'>
                <h3 className='card-title font-bold'>{post.title}</h3>
                <p className='text-sm text-gray-500'>
                  Posted by {post.username} on{' '}
                  {new Date(post.datePosted).toLocaleString()}
                </p>
                <p className='card-text p-2 mb-2'>{nl2br(post.content)}</p>
              </div>

              <div className='mb-2'>
                {/* Like OR Unlike button */}
                {post.likes.includes(username) ? (
                  <button
                    className='bg-white-500 text-blue-500 border border-blue-500 px-2 py-1 rounded mt-2 mr-1 mb-2'
                    onClick={() => handleUnlikePost(post._id)}
                  >
                    {post.number_of_likes} Unlike
                  </button>
                ) : (
                  <button
                    className='bg-blue-500 text-white px-2 py-1 rounded mt-2 mr-1 mb-2'
                    onClick={() => handleLikePost(post._id)}
                  >
                    {post.number_of_likes} Like
                  </button>
                )}

                {post.number_of_comments > 0 ? (
                showComments === false ? (
                  <button
                    className='text-orange underline px-2 py-1 rounded mt-2 mb-2'
                    onClick={() => setShowComments(true)}
                  >
                    Show {post.number_of_comments} Comment
                    {post.number_of_comments > 1 && 's'}
                  </button>
                  ) : (
                  <button
                    className='text-black underline px-2 py-1 rounded mt-2 mb-2'
                    onClick={() => setShowComments(false)}
                  >
                    Hide Comment
                    {post.number_of_comments > 1 && 's'}
                  </button>
                  )
                ) : (
                  <p className='text-gray underline inline px-2 py-1 rounded mt-2 mb-2'>
                    No Comments
                  </p>
                )}

                {/* Comment input field */}
                {showComments === true &&
                <>
                <textarea
                  className='w-full border-orange rounded p-2'
                  rows='2'
                  placeholder='Leave a comment'
                  value={newCommentText}
                  onChange={(e) => setNewCommentText(e.target.value)}
                ></textarea>

                {/* Comment button */}
                <button
                  className='bg-green text-white px-2 py-1 rounded mt-2'
                  onClick={() => handlePostComment(post._id)}
                >
                  Comment
                </button>

              {/* Display comments */}
              <div>
                {post.comments &&
                  post.comments.map((comment) => (
                    <div
                      key={comment._id}
                      className='border border-gray-300 rounded p-2 mb-2'
                    >
                      <p className='text-xs text-gray-700'>
                        Posted by {comment.username} on{' '}
                        {new Date(comment.date_posted).toLocaleString()}
                      </p>
                      <p>{nl2br(comment.body)}</p>

                      {/* Add delete comment button */}
                      <button
                        className='text-xs text-red-500 mt-1'
                        onClick={() =>
                          handleDeleteComment(post._id, comment._id)
                        }
                      >
                        Delete
                      </button>
                    </div>
                  ))}
              </div>
            </>}
          </div>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
}

export default Posts;
