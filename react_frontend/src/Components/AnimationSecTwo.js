import React from 'react';
import Community from '../Assets/images/community.jpg';
import '../index.css';
import { Link } from 'react-router-dom';

function AnimationSecTwo() {
  return (
    <figure className='relative flex justify-center items-center h-full'>
      <img
        className='community-img rounded-xl object-fit object-center mt-2 '
        src={Community}
        alt='community'
      />
      <figcaption className='absolute flex flex-col justify-center items-center mx-5 p-5 rounded-xl border border-white bg-white/75 shadow-lg shadow-black/5 saturate-200'>
        <h1
          className='text-center display-1 font-bold text-green mb-4'
        >
          Join A Wonderful Community
        </h1>
        <Link
          to='/register'
          className='p-2 text-white font-semibold text-lg hover:underline bg-green border border-black rounded'
        >
          Sign Up Now
        </Link>
      </figcaption>
    </figure>
  );
}

export default AnimationSecTwo;
