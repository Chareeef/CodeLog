import React from "react";
import Navigation from "./Navigation";
// import "../index.css"
import Footer from "./Footer";
import "../App.css";
import Animation from "./Animation";
import AnimationSecTwo from "./AnimationSecTwo";
import AnimationSecThree from "./AnimationSecThree";

const Home = () => {
  return (
    <div className="home-container">
      {/* <Navigation /> */}
      <Animation />
      {/* <AnimationSecTwo /> */}
      <AnimationSecThree />
      <Footer />
      
    </div>
  );
};
export default Home;
