import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import apiClient from '../apiClient';
import Navigation from './Navigation';
import Footer from './Footer';

function UpdateInfo() {
  const [newEmail, setNewEmail] = useState('');
  const [newUsername, setNewUsername] = useState('');
  const [updateUsername, setUpdateUsername] = useState('');
  const [updateEmail, setUpdateEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const updateInfo = async (event) => {
    event.preventDefault();

    const Data = {
      newEmail: newEmail,
      newUsername: newUsername,
    };

    try {
      const response = await apiClient.put('/me/update_infos', Data);

      if (response.status == 201) {
        alert('Your email and/or username updated successfully !');
        navigate('/profile');
      } else {
        alert('Something went wrong');
      }
    } catch (error) {
      if (error.response) {
        setMessage(`Error: ${error.response.data.error}`);
      } else {
        setMessage('An error occurred. Please try again later.');
      }
    }
  };

  return (
    <>
      <Navigation />
      <div className='d-flex flex-column min-vh-100'>
        <div className='bg-beige flex-1 flex-grow-1 d-flex flex-column justify-content-center'>
          <div className='sm:mx-auto sm:w-full sm:max-w-sm'>
            <h2 className='mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-black	text-900'>
              Update your information
            </h2>
          </div>
          <div className='mt-10 sm:mx-auto sm:w-full sm:max-w-sm'>
            {message && (
              <div className='alert alert-danger mb-2' role='alert'>
                {message}
              </div>
            )}
            <form className='space-y-6' onSubmit={updateInfo}>
              <div>
                <div className='mb-4 flex items-center'>
                  <input
                    type='checkbox'
                    id='userName'
                    checked={updateUsername}
                    onChange={(e) => setUpdateUsername(e.target.checked)}
                    className='form-checkbox h-5 w-5 text-blue-600'
                  />
                  <label htmlFor='userName' className='ml-2 text-gray-700'>
                    Username
                  </label>
                </div>
                {updateUsername && (
                  <>
                    {/* <div>
                    <label
                      htmlFor='email'
                      className='block text-sm font-medium leading-6 text-black text-900'
                    >
                      Email address
                    </label>
                    <div className='mt-2'>
                      <input
                        onChange={(e) => setEmail(e.target.value)}
                        value={email}
                        placeholder='email'
                        id='email'
                        name='email'
                        type='email'
                        autoComplete='email'
                        className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                        // required
                      />
                    </div>
                  </div> */}
                    <div>
                      <label
                        htmlFor='username'
                        className='block text-sm font-medium leading-6 text-black text-900'
                      >
                        New Username
                      </label>
                      <div className='mt-2'>
                        <input
                          onChange={(e) => setNewUsername(e.target.value)}
                          value={newUsername}
                          placeholder='username'
                          id='username'
                          name='username'
                          type='username'
                          autoComplete='username'
                          className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                          required
                        />
                      </div>
                    </div>
                  </>
                )}
              </div>
              <div>
                <div className='mb-4 flex items-center'>
                  <input
                    type='checkbox'
                    id='updateEmail'
                    checked={updateEmail}
                    onChange={(e) => setUpdateEmail(e.target.checked)}
                    className='form-checkbox h-5 w-5 text-blue-600'
                  />
                  <label htmlFor='userName' className='ml-2 text-gray-700'>
                    Email Address
                  </label>
                </div>
                {updateEmail && (
                  <>
                    {/* <div>
                    <label
                      htmlFor='email'
                      className='block text-sm font-medium leading-6 text-black text-900'
                    >
                      Email address
                    </label>
                    <div className='mt-2'>
                      <input
                        // onChange={(e) => setEmail(e.target.value)}
                        // value={email}
                        placeholder='email'
                        id='email'
                        name='email'
                        type='email'
                        autoComplete='email'
                        className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                        required
                      />
                    </div>
                  </div> */}
                    <div>
                      <label
                        htmlFor='email'
                        className='block text-sm font-medium leading-6 text-black text-900'
                      >
                        New Email Address
                      </label>
                      <div className='mt-2'>
                        <input
                          onChange={(e) => setNewEmail(e.target.value)}
                          value={newEmail}
                          placeholder='email'
                          id='email'
                          name='email'
                          type='email'
                          autoComplete='email'
                          className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                          required
                        />
                      </div>
                    </div>
                  </>
                )}
              </div>
              <button
                className='inline-block bg-green hover:bg-glight text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-2'
                type='submit'
              >
                Update Profile
              </button>
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}

export default UpdateInfo;
