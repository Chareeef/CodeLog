import React from 'react';

const Comment = ({ user, content }) => {
  return (
    <div className="comment">
      <p><strong>{user}:</strong> {content}</p>
    </div>
  );
}

export default Comment;
