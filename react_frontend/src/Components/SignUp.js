import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../index.css';
import apiClient from '../apiClient';
import Footer from './Footer';

function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const registerUser = async (event) => {
    event.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!username) {
      setMessage('Please enter your username');
    } else if (!email) {
      setMessage('Please enter you email');
    } else if (!emailRegex.test(email)) {
      setMessage('Invalid email');
    } else if (password.length < 6) {
      setMessage('Password must include at least 6 characters');
    } else {
      const data = {
        username: username,
        email: email,
        password: password,
      };

      try {
        await apiClient.post('/register', data);

        alert(`Great to meet you ${username}! You can Log In now!`);
        navigate('/login');
      } catch (error) {
        if (error.response) {
          setMessage(`Error: ${error.response.data.error}`);
        } else {
          setMessage('An error occurred. Please try again later.');
        }
      }
    }
  };

  return (
    <div className='d-flex flex-column min-vh-100'>
      <div className='bg-beige flex-1 flex-grow-1 d-flex flex-column justify-content-center'>
        <div className='sm:mx-auto sm:w-full sm:max-w-sm'>
          <h2 className='mt-10 text-center text-2xl font-bold leading-9 tracking-tight  text-black	text-900'>
            Create your account
          </h2>
        </div>

        <div className='mt-10 sm:mx-auto sm:w-full sm:max-w-sm'>
          {message && (
            <div className='alert alert-danger mb-2' role='alert'>
              {message}
            </div>
          )}

          <form onSubmit={registerUser} className='space-y-6'>
            <div>
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
                  required
                />
              </div>
            </div>

            <div>
              <label
                htmlFor='username'
                className='block text-sm font-medium leading-6 text-black text-900'
              >
                Username
              </label>
              <div className='mt-2'>
                <input
                  onChange={(e) => setUsername(e.target.value)}
                  value={username}
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
              <div className='flex items-center justify-between'>
                <label
                  htmlFor='password'
                  className='block text-sm font-medium leading-6 text-black text-900'
                >
                  Password
                </label>
                <div className='text-sm'></div>
              </div>
              <div className='mt-2'>
                <input
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                  placeholder='password'
                  id='password'
                  name='password'
                  type='password'
                  autoComplete='current-password'
                  minLength='6'
                  className='block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
                  required
                />
              </div>
            </div>

            <div>
              <button
                type='submit'
                className='flex w-full justify-center rounded-md bg-green px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-glight focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
              >
                Sign up
              </button>
            </div>
          </form>

          <p className='mt-10 text-center text-sm text-black text-500'>
            Already have an account?
            <br />
            <a
              href='/login'
              className='font-bold leading-6 text-orange text-600 hover:text-indigo-500'
            >
              Log in
            </a>
          </p>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default SignUp;
