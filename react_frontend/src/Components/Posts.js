import React, { useState, useEffect } from 'react';
import nl2br from 'react-nl2br';

import apiClient from '../apiClient';
import Footer from './Footer';

function Posts() {
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState({});
  const [newCommentText, setNewCommentText] = useState('');

  // Function to fetch posts from the backend API
  const fetchPosts = async () => {
    try {
      const res = await apiClient.get('/feed/get_posts');
      const posts = res.data;
      // fetch comments
      posts.forEach(async (p) => {
        console.log(posts);
        if (p.comments) {
          try {
            const res = await apiClient.post('/feed/post_comments', {
              post_id: p._id,
            });
            p.comments = res.data.data;
          } catch (error) {
            console.error(error);
          }
        }
      });
      console.log('final  :', posts);
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

              {/* Comment input field */}
              <div className='mb-2'>
                <textarea
                  className='w-full border-orange rounded p-2'
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
                {post.comments &&
                  post.comments.map((comment) => (
                    <div
                      key={comment._id}
                      className='border border-gray-300 rounded p-2 mb-2'
                    >
                      <p>body-0> {nl2br(comment.body)}</p>
                      <p className='text-xs text-gray-500'>
                        Posted by {comment.username} on{' '}
                        {new Date(comment.date_posted).toLocaleString()}
                      </p>
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
            </div>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
}

export default Posts;
