import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import apiClient from '../apiClient';
import Navigation from './Navigation';
import Footer from './Footer';

function UpdateInfo() {
  const [userInfo, setUserInfo] = useState({ email: '', username: '' });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await apiClient.get('/me/get_infos');

        setUserInfo(response.data);

        if (response.status === 200) {
          setUserInfo(response.data);
        }
      } catch (error) {
        console.error('Error fetching profile information:', error);
      }
    };
    fetchUserInfo();
  }, []);
  const handleChange = (event) => {
    const { name, value } = event.target;
    setUserInfo((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await apiClient.put('/me/update_infos', userInfo);

      if (response.status == 201) {
        navigate('/profile', {
          state: { successMessage: 'Your infos were updated successfully !' },
        });
      } else {
        alert('Something went wrong');
      }
    } catch (error) {
      if (error.response) {
        setMessage(`${error.response.data.error}`);
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
          <div className='mt-10 sm:mx-auto sm:w-full sm:max-w-sm'>
            {message && (
              <div className='alert alert-danger mb-2' role='alert'>
                {message}
              </div>
            )}

            <form className='space-y-6' onSubmit={handleSubmit}>
              <div>
                <label
                  htmlFor='email'
                  className='block text-sm font-medium leading-6 text-black text-900'
                >
                  Email address
                </label>
                <div className='mt-2'>
                  <input
                    onChange={handleChange}
                    value={userInfo.email}
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

              <div>
                <div className='flex items-center justify-between'>
                  <label
                    htmlFor='username'
                    className='block text-sm font-medium leading-6 text-black text-900'
                  >
                    Username
                  </label>
                </div>
                <div className='mt-2'>
                  <input
                    onChange={handleChange}
                    value={userInfo.username}
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

              <div>
                <button
                  type='submit'
                  className='flex w-full justify-center rounded-md bg-green px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-glight hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                >
                  Update Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}

export default UpdateInfo;
