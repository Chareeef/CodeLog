import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import nl2br from 'react-nl2br';

import apiClient from '../apiClient';
import Footer from './Footer';

function Profile() {
  const [userInfo, setUserInfo] = useState(null);
  const [userPosts, setUserPosts] = useState([]);
  const navigate = useNavigate();

  const check_auth = async () => {
    try {
      await apiClient.get('/');
    } catch (error) {
      console.error(error);
      alert(
        'Sorry, it seems your Authentication was lost or corrupted. Please log in again.'
      );
      localStorage.removeItem('jwt_access_token');
      localStorage.removeItem('jwt_refresh_token');
      navigate('/login');
    }
  };

  const fetchProfileInfo = async () => {
    try {
      const response = await apiClient.get('/me/get_infos');

      if (response.status === 200) {
        setUserInfo(response.data);
      }
    } catch (error) {
      console.error('Error fetching profile information:', error);
    }
  };

  const fetchUserPosts = async () => {
    try {
      const response = await apiClient.get('/me/posts');

      if (response.status === 200) {
        setUserPosts(response.data);
      }
    } catch (error) {
      console.error('Error fetching user posts:', error);
    }
  };

  useEffect(() => {
    check_auth();
    fetchProfileInfo();
    fetchUserPosts();
  }, []);

  const handleDeleteAccount = async () => {
    try {
      const response = await apiClient.delete('/me/delete_user');

      if (response.status === 200) {
        // Handle success, e.g., redirect to login page
      }
    } catch (error) {
      console.error('Error deleting user account:', error);
    }
  };



  return (
    <div className='d-flex flex-column min-vh-100'>
      <div className='bg-beige flex-1 flex-grow-1 d-flex flex-column justify-content-center p-3'>
        <h1 className='text-3xl font-semibold mb-4 mt-2'>
          Welcome to your space {userInfo && userInfo.username}!
        </h1>

        <div className='bg-white rounded-lg shadow-lg p-6 mb-8'>
          {userInfo ? (
            <>
              <h2 className='text-xl font-semibold'>User Profile</h2>
              <p>Email: {userInfo.email}</p>
              <p>Username: {userInfo.username}</p>
              <button
                onClick={handleDeleteAccount}
                className='inline-block bg-orange hover:bg-olight text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-2 mt-3'
              >
                Delete Account
              </button>
              <button
                // onClick={handleDeleteAccount}
                className='inline-block bg-orange hover:bg-olight text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-2 ml-4'
              >
                <a
                href='/update_password'>Update Password</a>
                
              </button>
              <button
                // onClick={handleDeleteAccount}
                className='inline-block bg-orange hover:bg-olight text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-2 ml-4'
              >
                <a
                href='/update_infos'>Update Information</a>
                
              </button>
              
            </>
          ) : (
            <p>Loading user information...</p>
          )}
        </div>

        <div className='bg-white rounded-lg shadow-lg p-6'>
          <h2 className='text-xl font-semibold'>User Posts</h2>
          {userPosts.length > 0 ? (
            <ul>
              {userPosts.map((post) => (
                <li className='card m-2' key={post._id}>
                  <div className='card-body'>
                    <h3 className='card-title font-bold'>{post.title}</h3>
                    <p className='text-sm text-gray-500'>
                      Posted on {new Date(post.datePosted).toLocaleString()}
                    </p>
                    <p className='card-text mt-2'>{nl2br(post.content)}</p>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>No posts found.</p>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Profile;
