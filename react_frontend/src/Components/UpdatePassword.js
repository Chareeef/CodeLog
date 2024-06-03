import React, { useState } from 'react';
import apiClient from '../apiClient';
import { useNavigate } from 'react-router-dom';

import Navigation from './Navigation';
import Footer from './Footer';

function UpdatePassword() {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  const UpdatePass = async (event) => {
    event.preventDefault();

    if (confirmPassword !== newPassword) {
      setMessage('New password and Confirm password do not match');
    } else {
      // conditions
      const Data = {
        old_password: oldPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
      };

      try {
        const response = await apiClient.put('/me/update_password', Data);

        if (response.status == 201) {
          navigate('/profile', {
            state: {
              successMessage: 'Your password was updated successfully !',
            },
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
    }
  };

  return (
    <>
      <Navigation />
      <div className='d-flex flex-column min-vh-100'>
        <div className='bg-beige flex-1 flex-grow-1 d-flex flex-column justify-content-center'>
          <div className='sm:mx-auto sm:w-full sm:max-w-sm'>
            <h2 className='mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-black	text-900'>
              Update Your Password
            </h2>
          </div>
          <div className='mt-10 sm:mx-auto sm:w-full sm:max-w-sm'>
            {message && (
              <div className='alert alert-danger mb-2' role='alert'>
                {message}
              </div>
            )}
            <form className='space-y-6' onSubmit={UpdatePass}>
              <div>
                <label
                  htmlFor='password'
                  className='block text-sm font-medium leading-6 text-black text-900'
                >
                  Old Password
                </label>
                <div className='mt-2'>
                  <input
                    onChange={(e) => setOldPassword(e.target.value)}
                    value={oldPassword}
                    placeholder='Old Password'
                    id='password'
                    name='password'
                    type='password'
                    minLength='6'
                    className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                    required
                  />
                </div>
              </div>
              <div>
                <div className='flex items-center justify-between'>
                  <label
                    htmlFor='new-password'
                    className='block text-sm font-medium leading-6 text-black text-900'
                  >
                    New Password
                  </label>
                </div>
                <div className='mt-2'>
                  <input
                    onChange={(e) => setNewPassword(e.target.value)}
                    value={newPassword}
                    placeholder='New Password'
                    id='new-password'
                    name='new-password'
                    type='password'
                    minLength='6'
                    className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                    required
                  />
                </div>
              </div>
              <div>
                <div className='flex items-center justify-between'>
                  <label
                    htmlFor='confirm-password'
                    className='block text-sm font-medium leading-6 text-black text-900'
                  >
                    Confirm Password
                  </label>
                </div>
                <div className='mt-2'>
                  <input
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    value={confirmPassword}
                    placeholder='Confirm Password'
                    id='confirm-password'
                    name='confirm-password'
                    type='password'
                    minLength='6'
                    className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                    required
                  />
                </div>
              </div>
              <button
                className='flex w-full justify-center rounded-md bg-green px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-glight hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                type='submit'
              >
                Update Password
              </button>
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}

export default UpdatePassword;
