import Navigation from './Navigation';
import Animation from './Animation';

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
        {/* <AnimationSecTwo /> 
        <AnimationSecThree />
        <Footer /> */}
      </div>
    </>
  );
}

export default LandingPage;
