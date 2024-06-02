// create home page to let user share a post
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../index.css';
import apiClient from '../apiClient';
import { formatTime } from '../utils';
import Footer from './Footer';

function Home() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const check_auth = async () => {
      try {
        await apiClient.get('/');
      } catch (error) {
        console.error(error);
        navigate('/login');
        alert(
          'Sorry, it seems your Authentication was lost or corrupted. Please log in again.'
        );
        localStorage.removeItem('jwt_access_token');
        localStorage.removeItem('jwt_refresh_token');
      }
    };

    check_auth();
  }, []);

  useEffect(() => {
    const fetchStreaks = async () => {
      try {
        const response = await apiClient.get('/me/streaks');
        const ttl = response.data.ttl;

        if (ttl > 8 * 3600) {
          const expirationTimestamp = new Date().getTime() + (ttl - 8 * 3600) * 1000;
          let remainingTime = expirationTimestamp - new Date().getTime();

          const countdownInterval = setInterval(() => {
            remainingTime -= 1000;
            if (remainingTime <= 0) {
              clearInterval(countdownInterval);
              setMessage('');
            } else {
              const timeString = formatTime(remainingTime);
              setMessage(`You must wait ${timeString} to post again.`);
            }
          }, 1000);

          return () => clearInterval(countdownInterval);
        }
      } catch (error) {
        console.error(error);
      }
    };

    fetchStreaks();
  }, []);

  const handleUserPost = async (event) => {
    event.preventDefault();

    const data = {
      title: title,
      content: content,
      is_public: isPublic,
    };

    try {
      const response = await apiClient.post('/log', data);

      if (response.status == 201) {
        alert('Posted successfully!');
      } else {
        alert('Something went wrong');
      }

      navigate('/profile');
    } catch (error) {
      alert(error.response.data.error);
    }
  };
  return (
    <>
      <div className='bg-beige flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8 post-log'>
        <h2 className='mt-10 text-center text-3xl font-bold leading-9 tracking-wide text-black'>
          Behind the Code: Your Journey Matters
        </h2>
        <form onSubmit={handleUserPost}>
          <div className='mb-4'>
            <label
              className='block text-black text-sm font-bold mb-2'
              htmlFor='title'
            >
              Title
            </label>
            <input
              className='appearance-none border rounded w-full py-2 px-3 text-gray-900 leading-tight focus:outline-none focus:shadow-outline'
              id='title'
              type='text'
              placeholder='Enter title'
              minLength='6'
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>
          <div className='mb-4'>
            <textarea
              className='w-full p-4 text-base text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500'
              id='journey'
              rows='10'
              minLength='150'
              placeholder='Write your journey here...'
              required
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>
          </div>
          <div className='mb-4 flex items-center'>
            <input
              type='checkbox'
              id='isPublic'
              checked={isPublic}
              onChange={(e) => setIsPublic(e.target.checked)}
              className='form-checkbox h-5 w-5 text-blue-600'
            />
            <label htmlFor='isPublic' className='ml-2 text-gray-700'>
              Public
            </label>
          </div>

          <button
            className='inline-block bg-green hover:bg-glight text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-2'
            type='submit'
          >
            Submit
          </button>
        </form>
        {message && (
          <div className='alert alert-danger mb-2' role='alert'>
            {message}
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}

export default Home;
