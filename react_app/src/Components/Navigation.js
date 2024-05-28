import { useEffect, useState } from 'react';
import { faBars, faFire } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate } from 'react-router-dom';

import apiClient from '../apiClient';

const Navigation = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [longStreaks, setLongStreaks] = useState(0);
  const [currStreaks, setCurrStreaks] = useState(0);

  const navigate = useNavigate();

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
