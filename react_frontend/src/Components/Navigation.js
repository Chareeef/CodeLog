import { useEffect, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faFireFlameSimple,
  faFireFlameCurved,
} from '@fortawesome/free-solid-svg-icons';
import { Link, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

import '../Assets/Navstyle.css';
import { checkAuth, formatTime } from '../utils';
import apiClient from '../apiClient';

const Navigation = ({ publicComp }) => {
  const [longStreak, setLongStreak] = useState(0);
  const [currentStreak, setCurrentStreak] = useState(0);
  const [expireTime, setExpireTime] = useState(0);
  const [remainingTime, setRemainingTime] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    if (publicComp !== true) {
      checkAuth(navigate);
    }
  }, []);

  useEffect(() => {
    const getStreaks = async () => {
      try {
        const res = await apiClient.get('/me/streaks');

        setCurrentStreak(res.data.current_streak);
        setLongStreak(res.data.longest_streak);

        const ttl = res.data.ttl;
        if (ttl > 0) {
          const expirationTimestamp = new Date().getTime() + ttl * 1000;
          setExpireTime(expirationTimestamp);
          setRemainingTime(expirationTimestamp - new Date().getTime());
        }
      } catch (error) {
        console.error(error);
      }
    };

    getStreaks();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const currentTime = new Date().getTime();
      const timeLeft = expireTime - currentTime;
      setRemainingTime(timeLeft);

      if (timeLeft <= 0) {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [expireTime]);

  const handleLogOut = async (event) => {
    event.preventDefault();

    try {
      const response = await apiClient.post('/logout');
      console.log(response);
    } catch (error) {
      console.error(error);
    }

    localStorage.removeItem('jwt_access_token');
    localStorage.removeItem('jwt_refresh_token');

    navigate('/login', {
      state: { successMessage: 'Successfully Logged Out' },
    });
  };

  return (
    <nav className='nav'>
      <a href='/' className='site-title '>
        CodeLog
      </a>
      <div className='navbar-links-container'>
        <ul>
          {localStorage.getItem('jwt_access_token') ? (
            <>
              <li>
                <Link
                  to='/feed'
                  className='site-navitem1 font-lg hover:font-xl hover:text-purple-700'
                >
                  Feed
                </Link>
              </li>
              <li>
                <Link
                  to='/profile'
                  className='site-navitem4 font-lg hover:font-xl hover:text-purple-700'
                >
                  Profile
                </Link>
              </li>
              <li>
                <FontAwesomeIcon icon={faFireFlameCurved} /> {longStreak}
              </li>
              <li>
                <FontAwesomeIcon icon={faFireFlameSimple} />{' '}
                {remainingTime > 0
                  ? `${currentStreak} (${formatTime(remainingTime)})`
                  : '0'}
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
                <Link to='/login'>Sign In</Link>
              </li>
              <li>
                <Link to='/register'>Sign Up</Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

Navigation.propTypes = {
  publicComp: PropTypes.bool,
};

Navigation.defaultProps = {
  publicComp: false,
};

export default Navigation;
