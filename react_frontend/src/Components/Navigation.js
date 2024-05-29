import { useEffect, useState } from 'react';
import { faBars, faFire } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate } from 'react-router-dom';

import '../Assets/Navstyle.css';
import apiClient from '../apiClient';

const Navigation = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [longStreaks, setLongStreaks] = useState(0);
  const [currStreaks, setCurrStreaks] = useState(0);

  const navigate = useNavigate();

  async () => {
    try {
      const res = await apiClient.get('/');
      console.log(res.data);
    } catch (error) {
      try {
        const res = await apiClient.post('/refresh');
        console.log(res.data);
        localStorage.setItem('jwt_access_token', res.data.new_access_token);
      } catch (error) {
        localStorage.removeItem('jwt_access_token');
        localStorage.removeItem('jwt_refresh_token');
      }
    }
  };

  const handleLogOut = async (event) => {
    event.preventDefault();

    try {
      const response = await apiClient.post('/logout');

      console.log(response);
      if (response.status == 204) {
        localStorage.removeItem('jwt_access_token');
        localStorage.removeItem('jwt_refresh_token');
        alert('Successfully Logged Out');
        navigate('/login');
      } else {
        alert('Failed to Log Out');
      }
    } catch (error) {
      alert('Failed to Log Out');
      console.error(error);
    }
  };

  useEffect(() => {
    apiClient
      .get('/me/streaks')
      .then((res) => {
        setCurrStreaks(res.data.current_streak);
        setLongStreaks(res.data.longest_streak);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <nav className='nav'>
      <a href='/' className='site-title'>
        SoftwareSphere
      </a>
      <a
        href='/'
        className='site-navitem1 font-lg hover:font-xl hover:text-purple-700'
      >
        Posts
      </a>
      <a
        href='/'
        className='site-navitem2 font-lg hover:font-xl hover:text-purple-700'
      >
        Longest Streak
      </a>
      <a
        href='/'
        className='site-navitem3 font-lg hover:font-xl hover:text-purple-700'
      >
        Debug Corner
      </a>
      <a
        href='/'
        className='site-navitem4 font-lg hover:font-xl hover:text-purple-700'
      >
        Profile
      </a>
      <div className='navbar-links-container'>
        <ul className={showMenu ? 'open' : ''}>
          {localStorage.getItem('jwt_access_token') ? (
            <>
              <li>
                <FontAwesomeIcon icon={faFire} /> (Longest {longStreaks})
              </li>
              <li>
                <FontAwesomeIcon icon={faFire} /> (Current {currStreaks})
              </li>
              <li>
                <Link to='/home'>Home</Link>
              </li>
              <li>
                <Link to='/' onClick={handleLogOut}>
                  Log Out
                </Link>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to='/login'>Sign-in</Link>
              </li>
              <li>
                <Link to='/register'>Sign-up</Link>
              </li>
            </>
          )}
        </ul>
      </div>
      <FontAwesomeIcon
        className='menu'
        onClick={() => {
          setShowMenu(!showMenu);
        }}
        icon={faBars}
      />
    </nav>
  );
};

export default Navigation;
