import React from 'react';
import Navigation from './Navigation';
import Animation from './Animation';
import AnimationSecTwo from './AnimationSecTwo';
import AnimationSecThree from './AnimationSecThree';
import Footer from './Footer';

import '../App.css';
// import AnimationSecTwo from './AnimationSecTwo';
// import AnimationSecThree from './AnimationSecThree';
// import Footer from './Footer';

function LandingPage() {
  return (
    <>
      <div className='home-container'>
        <Navigation />
        <Animation />
        <AnimationSecTwo /> 
        <AnimationSecThree />
        <Footer /> 
      </div>
    </>
  );
}

export default LandingPage;
