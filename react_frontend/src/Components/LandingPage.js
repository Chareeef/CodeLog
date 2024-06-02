import React from 'react';
import Navigation from './Navigation';
import Animation from './Animation';
import AnimationSecTwo from './AnimationSecTwo';
import AnimationSecThree from './AnimationSecThree';
import Footer from './Footer';
import '../App.css';

function LandingPage() {
  return (
    <>
      <div className='home-container'>
        <Navigation publicComp={true} />
        <Animation />
        <AnimationSecTwo />
        <AnimationSecThree />
        <Footer />
      </div>
    </>
  );
}

export default LandingPage;
