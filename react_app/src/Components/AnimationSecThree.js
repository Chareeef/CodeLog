import React from 'react';
import { LinkIcon, PuzzlePieceIcon, MegaphoneIcon, UsersIcon } from '@heroicons/react/24/outline'
import '../index.css';
// import { motion } from 'framer-motion';

const features = [
  {
    name: 'Connect with Peers',
    description:
      'Network with like-minded developers, share your experiences, and build meaningful professional relationships.',
    icon: LinkIcon,
  },
  {
    name: 'Express Your Needs',
    description:
      'Voice your challenges and requirements, and get support from a community that understands and can offer solutions.',
    icon: PuzzlePieceIcon,
  },
  {
    name: 'Share Your Thoughts',
    description:
      'Engage in insightful discussions, share your knowledge, and stay updated with the latest trends and best practices in the industry.',
    icon: MegaphoneIcon,
  },
  {
    name: 'Collaborate on Projects',
    description:
      'Team up with other developers to work on exciting projects, learn new skills, and create something amazing together.',
    icon: UsersIcon,
  },
]
function AnimationSecThree() {
  return (
    <div className=' bg-beige'>
      <div className=' w-screen mx-auto  px-6 lg:px-8  container-three'>
        <div className='mx-auto max-w-2xl lg:text-center'>
          <h2 className='mt-2 pt-4 text-8xl font-bold tracking-tight text-brown sm:text-6xl'>
            Become A Memeber
          </h2>
          <p className='mt-6 text-lg leading-8 text-gray-800'>
            we build this space to let developers connect with each other,
            express their needs, share their toughts and why not collaborate
            with each other to create an amazing project.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16 pb-4">
            {features.map((feature) => (
              <div key={feature.name} className="relative pl-16">
                <dt className=" font-semibold leading-7 text-brown text-lg">
                  {feature.icon && (
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-orange">
                    <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                  </div>
                  )}
                  {feature.name}
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">{feature.description}</dd>
              </div>
            ))}
          </dl>
          </div>
      </div>
    </div>
  );
}

export default AnimationSecThree;
