import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import './Assets/Navstyle.css';
import LandingPage from './Components/LandingPage';
import SignIn from './Components/SignIn';
import SignUp from './Components/SignUp';
import Home from './Components/Home';
import Navigation from './Components/Navigation';
import Posts from './Components/Posts';
import Profile from './Components/Profile';
import UpdatePassword from './Components/UpdatePassword';
import UpdateInfo from './Components/UpdateInfo';

function App() {
  return (
    <Router>
      <div className='App'>
        <Navigation />
        <div className='content'>
          <Routes>
            <Route path='/' element={<LandingPage />} />
            <Route path='/home' element={<Home />} />
            <Route path='/login' element={<SignIn />} />
            <Route path='/register' element={<SignUp />} />
            <Route path='/posts' element={<Posts />} />
            <Route path='/profile' element={<Profile />} />
            <Route path='/update_password' element={<UpdatePassword />} />
            <Route path='/update_infos' element={<UpdateInfo />} />

          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
