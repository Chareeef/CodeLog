import React from 'react';
import '../index.css';

function Posts() {
  return (
    <div className='container'>
      <div className='submission-box'>
        <h3>How was your coding Journey today?</h3>
        <form action='submit_post.php' method='post'>
          <input type='text' name='title' placeholder='Post Title' required />
          <textarea
            name='content'
            rows='5'
            placeholder='Write your post here...'
            required
          ></textarea>
          <input type='submit' value='Submit Post' />
        </form>
      </div>

      <div className='posts'>
        {/* Example post */}
        <div className='post'>
          <h3>Random Latin paragraph</h3>
          <p>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Excepturi
            necessitatibus officia voluptas! Sunt illum atque commodi. Tempore
            pariatur vel repellat explicabo, assumenda illo, ex eaque
            perspiciatis dolorum praesentium quaerat nam. Lorem ipsum dolor sit
            amet consectetur adipisicing elit. Iure ab unde magni. Aliquid earum
            qui neque, est vitae dolorem! Modi sequi, doloremque nam ut eos
            excepturi distinctio alias neque optio!
          </p>
          <div className='comments'>
            <h4>Comments</h4>
            <div className='comment'>
              <p>
                <strong>User1:</strong> This is a comment.
              </p>
            </div>
            <div className='comment-form'>
              <input type='text' placeholder='Add a comment...' />
              <input type='submit' value='Comment' />
            </div>
          </div>
        </div>
        <div className='post'>
          <h3>That Latin paragraph again</h3>
          <p>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Excepturi
            necessitatibus officia voluptas! Sunt illum atque commodi. Tempore
            pariatur vel repellat explicabo, assumenda illo, ex eaque
            perspiciatis dolorum praesentium quaerat nam. Lorem ipsum dolor sit
            amet consectetur adipisicing elit. Iure ab unde magni. Aliquid earum
            qui neque, est vitae dolorem! Modi sequi, doloremque nam ut eos
            excepturi distinctio alias neque optio!
          </p>
          <div className='comments'>
            <h4>Comments</h4>
            <div className='comment'>
              <p>
                <strong>User2:</strong> Another comment here.
              </p>
            </div>
            <div className='comment-form'>
              <input type='text' placeholder='Add a comment...' />
              <input type='submit' value='Comment' />
            </div>
          </div>
        </div>
        {/* Additional posts will be inserted here */}
      </div>
    </div>
  );
}

export default Posts;
