import React from 'react';
import './App.css';
import LandingPage from './Components/LandingPage';
import './Assets/Navstyle.css';
import SignIn from './Components/SignIn';
import SignUp from './Components/SignUp';
import Home from './Components/Home';
import Posts from './Components/Posts'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navigation from './Components/Navigation';

function App() {
  return (
    <Router>
      <div className='App'>
        <Navigation />
        <div className='content'>
          <Routes>
            <Route path='/' element={<LandingPage />} />
            <Route path='/login' element={<SignIn />} />
            <Route path='/register' element={<SignUp />} />
            <Route path='/home' element={<Home />} />
            <Route path='' element={<Posts />}/>
            {/* <Route path='' element={<LongestStreak />}/> */}
            <Route path='' element={<Posts />}/>
            <Route path='' element={<Posts />}/>

          </Routes>
        </div>

        {/* <Footer /> */}
      </div>
    </Router>
  );
}

export default App;
