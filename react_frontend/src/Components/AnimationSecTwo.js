import React from 'react';
import Community from '../Assets/images/com.jpg';
import '../index.css';
import Typography from '@mui/material/Typography';

function AnimationSecTwo() {
  return (
    <figure className='relative flex justify-center'>
      <img
        className='h-3/3 w-9/12 rounded-xl object-cover object-center mt-2'
        src={Community}
        alt='community'
      />
      <figcaption className='flex justify-center items-center pr-50 absolute bottom-1/2 left-2/4 flex w-[calc(100%-23.9rem)] -translate-x-2/4  rounded-xl border border-white bg-white/75 py-4 px-6 shadow-lg shadow-black/5 saturate-200 backdrop-blur-sm'>
        <Typography
          variant='h1'
          fontWeight='bold'
          className='mr-15 font-extrabold text-green text-xl'
        >
          We Are Community
        </Typography>
      </figcaption>
    </figure>
  );
}

export default AnimationSecTwo;
