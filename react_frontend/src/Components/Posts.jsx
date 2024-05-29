import React, { useEffect, useState } from 'react';
import { getPosts, likePost, unlikePost, addComment } from '../apiRequests';

const Posts = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const postsData = await getPosts();
      setPosts(postsData);
    };
    fetchPosts();
  }, []);

  const handleLike = async (postId) => {
    await likePost(postId);
    const updatedPosts = await getPosts();
    setPosts(updatedPosts);
  };

  const handleUnlike = async (postId) => {
    await unlikePost(postId);
    const updatedPosts = await getPosts();
    setPosts(updatedPosts);
  };

  const handleAddComment = async (postId, comment) => {
    await addComment(postId, comment);
    const updatedPosts = await getPosts();
    setPosts(updatedPosts);
  };

  return (
    <div>
      {posts.map((post) => (
        <div key={post._id}>
          <h2>{post.title}</h2>
          <p>{post.body}</p>
          <button onClick={() => handleLike(post._id)}>Like</button>
          <button onClick={() => handleUnlike(post._id)}>Unlike</button>
          <input
            type='text'
            placeholder='Add comment...'
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleAddComment(post._id, e.target.value);
            }}
          />
          <ul>
            {post.comments.map((comment) => (
              <li key={comment._id}>{comment.body}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default Posts;
