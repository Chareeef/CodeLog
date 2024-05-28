import { useState, useEffect } from 'react';
import apiProfile from '../apiProfile';

function Profile() {
  const [userInfo, setUserInfo] = useState(null);
  const [userPosts, setUserPosts] = useState([]);

  useEffect(() => {
    const fetchProfileInfo = async () => {
      try {
        const response = await apiProfile.get('/get_infos');

        if (response.status === 200) {
          setUserInfo(response.data);
        }
      } catch (error) {
        console.error('Error fetching profile information:', error);
      }
    };

    const fetchUserPosts = async () => {
      try {
        const response = await apiProfile.get('/posts');

        if (response.status === 200) {
          setUserPosts(response.data);
        }
      } catch (error) {
        console.error('Error fetching user posts:', error);
      }
    };

    fetchProfileInfo();
    fetchUserPosts();
  }, []);

  const handleDeleteAccount = async () => {
    try {
      const response = await apiProfile.delete('/delete_user');

      if (response.status === 200) {
        // Handle success, e.g., redirect to login page
      }
    } catch (error) {
      console.error('Error deleting user account:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-semibold mb-4">Welcome, {userInfo && userInfo.username}</h1>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        {userInfo ? (
          <>
            <h2 className="text-xl font-semibold">User Profile</h2>
            <p>Email: {userInfo.email}</p>
            <p>Username: {userInfo.username}</p>
            <button onClick={handleDeleteAccount} className="bg-red-500 text-white px-4 py-2 mt-4 rounded-lg">
              Delete Account
            </button>
          </>
        ) : (
          <p>Loading user information...</p>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold">User Posts</h2>
        {userPosts.length > 0 ? (
          <ul>
            {userPosts.map((post) => (
              <li key={post._id}>
                <h3>{post.title}</h3>
                <p>{post.body}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No posts found.</p>
        )}
      </div>
    </div>
  );
}

export default Profile;
