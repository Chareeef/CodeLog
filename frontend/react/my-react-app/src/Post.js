import React from 'react';
import Comment from './Comment';
import CommentForm from './CommentForm';

const Post = ({ title, content }) => {
  const exampleComments = [
    { user: 'User1', content: 'This is a comment.' },
    { user: 'User2', content: 'Another comment here.' }
  ];

  return (
    <div className="post">
      <h3>{title}</h3>
      <p>{content}</p>
      <div className="comments">
        <h4>Comments</h4>
        {exampleComments.map((comment, index) => (
          <Comment key={index} user={comment.user} content={comment.content} />
        ))}
        <CommentForm />
      </div>
    </div>
  );
}

export default Post;
