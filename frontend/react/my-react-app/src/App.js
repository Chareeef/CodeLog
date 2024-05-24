import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter, Route, and Routes
import Header from './Header';
import SubmissionBox from './SubmissionBox';
import Posts from './Posts';

const Home = () => {
  return (
    <div>
      <h2>Welcome to the Home Page!</h2>
      {/* You can add any additional content for your home page here */}
    </div>
  );
};

const About = () => {
  return (
    <div>
      <h2>About Us</h2>
      {/* You can add any additional content for your About page here */}
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <div className="App">
        <Header />
        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} /> {/* Route for the Home page */}
            <Route path="/posts" element={<Posts />} /> {/* Route for the Posts page */}
            <Route path="/about" element={<About />} /> {/* Route for the About page */}
          </Routes>
          {/* SubmissionBox can be shown on multiple pages, so it's not included in the routing */}
          <SubmissionBox />
        </div>
      </div>
    </Router>
  );
};

export default App;
