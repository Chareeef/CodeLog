import React from 'react';
import './index.css';

function Profile() {
  return (
    <div className='container'>
      <div className='profile-card'>
        <h2>Member Profile</h2>
        <form id='profile-form' action='#' method='post'>
          <div className='form-group'>
            <label htmlFor='name'>Name:</label>
            <input
              type='text'
              id='name'
              name='name'
              defaultValue='John Doe'
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor='email'>Email:</label>
            <input
              type='email'
              id='email'
              name='email'
              defaultValue='john@example.com'
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor='location'>Location:</label>
            <input
              type='text'
              id='location'
              name='location'
              defaultValue='New York, USA'
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor='password'>Password:</label>
            <input type='password' id='password' name='password' required />
          </div>
          <div className='form-group'>
            <label htmlFor='confirm-password'>Confirm Password:</label>
            <input
              type='password'
              id='confirm-password'
              name='confirm-password'
              required
            />
          </div>
          <div className='form-group'>
            <input type='submit' value='Save Changes' />
          </div>
        </form>
      </div>
    </div>
  );
}

export default Profile;
