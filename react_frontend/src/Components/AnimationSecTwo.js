import React from 'react';
import Community from '../Assets/images/com.jpg';
import '../index.css';
import Typography from '@mui/material/Typography';
import { Link } from 'react-router-dom';

function AnimationSecTwo() {
  return (
    <figure className='relative flex justify-center items-center h-full'>
      <img
        className='h-3/3 w-9/12 rounded-xl object-cover object-center mt-2'
        src={Community}
        alt='community'
      />
      <figcaption className='absolute w-50 flex flex-col justify-center items-center p-5 rounded-xl border border-white bg-white/75 shadow-lg shadow-black/5 saturate-200 backdrop-blur-sm'>
        <Typography
          variant='h1'
          fontWeight='bold'
          className='text-center font-bold text-green mb-4'
        >
          Join A Wonderful Community
        </Typography>
        <Link to='/register' className='p-2 text-white font-semibold text-lg hover:underline bg-green border border-black rounded'>
          Sign Up Now
        </Link>
      </figcaption>
    </figure>
  );
}

export default AnimationSecTwo;
