import React, {useState} from "react";
// import Logo from "../Assets/temp_logo.png";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';


const Navigation = () => {
  const [showMenu, setShowMenu] = useState(false)
  return (
    <nav className="nav">
      {/* <div className="nav-logo-container">
        <img src={Logo} alt="" width="40" height="40"/>
      </div> */}
      <a href="/" className="site-title">
        SoftwareSphere
      </a>
      <div className="navbar-links-container">
        <ul className={showMenu ? "open" : ""} >
          <li>
            <a href="/">Home</a>
          </li>
          <li>
            <a href="/sign-in">Sign-in</a>
          </li>
          <li>
            <a href="/register">Sign-up</a>
          </li>
        </ul>
      </div>
      <FontAwesomeIcon className="menu" onClick={() => {setShowMenu(!showMenu)}}
      icon={faBars} 
      />
    </nav>
    
  );
};

export default Navigation;
