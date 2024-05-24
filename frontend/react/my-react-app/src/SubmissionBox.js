import React from 'react';

const SubmissionBox = () => {
  return (
    <div className="submission-box">
      <h3>Write Your Own Post</h3>
      <form action="submit_post.php" method="post">
        <input type="text" name="title" placeholder="Post Title" required />
        <textarea name="content" rows="5" placeholder="Write your post here..." required></textarea>
        <input type="submit" value="Submit Post" />
      </form>
    </div>
  );
}

export default SubmissionBox;
