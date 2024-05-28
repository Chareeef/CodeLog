import React from 'react';
import './App.css';
import LandingPage from './Components/LandingPage';
import './Assets/Navstyle.css';
import SignIn from './Components/SignIn';
import SignUp from './Components/SignUp';
import Home from './Components/Home';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navigation from './Components/Navigation';
import CodeQuestions from './Components/CodeQuestions';
import Posts from './Components/Posts';
import Profile from './Components/Profile';
import LongestCodingStreaks from './Components/LongestCodingStreaks';

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
            <Route path='/log' element={<Home />} />
            <Route path='/posts' component={<Posts />} />
            <Route path='/profile' component={<Profile />} />
            <Route path='/longest-streak' component={<LongestCodingStreaks/>} />
            <Route path='/debug-corner' component={<CodeQuestions />} />
          </Routes>
        </div>
        {/* <Footer /> */}
      </div>
    </Router>
  );
}

export default App;
