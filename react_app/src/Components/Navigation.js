import React, { useState } from 'react';
import { Link } from 'react-router-dom';
// import Logo from "../Assets/temp_logo.png";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';

const Navigation = () => {
  const [showMenu, setShowMenu] = useState(false);
  return (
    <nav className='nav'>
      {/* <div className="nav-logo-container">
        <img src={Logo} alt="" width="40" height="40"/>
      </div> */}
      <a href='/' className='site-title'>
        SoftwareSphere
      </a>
      <div className='navbar-links-container'>
        <ul className={showMenu ? 'open' : ''}>
          <li>
            <Link to='/'>Home</Link>
          </li>
          <li>
            <Link to='/login'>Sign-in</Link>
          </li>
          <li>
            <Link to='/register'>Sign-up</Link>
          </li>
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
