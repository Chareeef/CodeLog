// create home page to let user share a post
import { useState } from 'react';

import '../index.css';
import apiClient from '../apiClient';

function Home() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [message, setMessage] = useState('');

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

      setTitle('');
      setContent('');
      setIsPublic(false);

    } catch (error) {
      console.error('Error:', error);
      setMessage(error.response.data.error);
    }
  };
  return (
    <>
      <div className='flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8'>
        <h2 className='mt-10 text-center text-3xl font-bold leading-9 tracking-wide text-white'>
          Behind the Code: Your Journey Matters
        </h2>
        <form onSubmit={handleUserPost}>
          <div className='mb-4'>
            <label
              className='block text-white text-sm font-bold mb-2'
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
            <label htmlFor='isPublic' className='ml-2 text-gray-700'>Public</label>
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
    </>
  );
}

export default Home;
