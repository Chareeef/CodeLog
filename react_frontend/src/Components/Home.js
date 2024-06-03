// create home page to let user share a post
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import '../index.css';
import apiClient from '../apiClient';
import { formatTime } from '../utils';
import Footer from './Footer';
import Navigation from './Navigation';

function Home() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const navigate = useNavigate();
  const locate = useLocation();

  useEffect(() => {
    const successMessage = locate.state?.successMessage;
    if (successMessage) {
      setSuccessMessage(successMessage);
    }
  }, []);

  useEffect(() => {
    const fetchStreaks = async () => {
      try {
        const response = await apiClient.get('/me/streaks');
        const ttl = response.data.ttl;
        const postsInterval =
          process.env.REACT_APP_ENV === 'DEV' ? 60 : 8 * 3600;

        if (ttl > postsInterval) {
          const expirationTimestamp =
            new Date().getTime() + (ttl - postsInterval) * 1000;
          let remainingTime = expirationTimestamp - new Date().getTime();

          const countdownInterval = setInterval(() => {
            remainingTime -= 1000;
            if (remainingTime <= 0) {
              clearInterval(countdownInterval);
              setAlertMessage('');
            } else {
              const timeString = formatTime(remainingTime);
              setAlertMessage(`You must wait ${timeString} to post again.`);
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
        navigate('/profile', {
          state: { successMessage: 'Posted successfully!' },
        });
      } else {
        alert('Something went wrong');
      }
    } catch (error) {
      alert(error.response.data.error);
    }
  };

  return (
    <>
      <Navigation />
      <div className='bg-beige flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8 post-log'>
        {successMessage && (
          <div className='alert alert-success mb-2' role='alert'>
            {successMessage}
          </div>
        )}

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
        {alertMessage && (
          <div className='alert alert-danger mb-2' role='alert'>
            {alertMessage}
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}

export default Home;
