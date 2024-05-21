import React from "react";
import Navigation from "./Navigation";
import World from "../Assets/world.jpg";
import "../App.css";

const Home = () => {
  return (
    <div className="home-container">
      <Navigation />
      <div className='container'>
        <section>
          <p>
            It is a long established fact that a reader will be distracted by
            the readable content of a page when looking at its layout. The point
            of using Lorem Ipsum is that it has a more-or-less normal
            distribution of letters, as opposed to using 'Content here, content
            here', making it look like readable English. Many desktop publishing
            packages and web
          </p>
          <img src={World} alt="" width="100" height="100"/>
        </section>
        <section>
          <p>
            It is a long established fact that a reader will be distracted by
            the readable content of a page when looking at its layout. The point
            of using Lorem Ipsum is that it has a more-or-less normal
            distribution of letters, as opposed to using 'Content here, content
            here', making it look like readable English. Many desktop publishing
            packages and web
          </p>
          <img src={World} alt="" width="100" height="100"/>
        </section>
        <section>
          <p>
            It is a long established fact that a reader will be distracted by
            the readable content of a page when looking at its layout. The point
            of using Lorem Ipsum is that it has a more-or-less normal
            distribution of letters, as opposed to using 'Content here, content
            here', making it look like readable English. Many desktop publishing
            packages and web
          </p>
          <img src={World} alt="" width="100" height="100"/>
        </section>
        <section>
          <p>
            It is a long established fact that a reader will be distracted by
            the readable content of a page when looking at its layout. The point
            of using Lorem Ipsum is that it has a more-or-less normal
            distribution of letters, as opposed to using 'Content here, content
            here', making it look like readable English. Many desktop publishing
            packages and web
          </p>
          <img src={World} alt="" width="100" height="100"/>
        </section>
      </div>
    </div>
  );
};
export default Home;
