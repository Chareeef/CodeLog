import React from 'react';
import Post from './Post';

const Posts = () => {
  const examplePosts = [
    { title: 'Post Title 1', content: 'Post content goes here. This is an example of a post written by a member.' },
    { title: 'Post Title 2', content: 'Another post content goes here. This is another example of a post written by a member.' }
  ];

  return (
    <div className="posts">
      {examplePosts.map((post, index) => (
        <Post key={index} title={post.title} content={post.content} />
      ))}
    </div>
  );
}
