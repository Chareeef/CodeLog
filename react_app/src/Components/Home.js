import React from "react";
import Navigation from "./Navigation";
// import "../index.css"
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
      
    </div>
  );
};
export default Home;
