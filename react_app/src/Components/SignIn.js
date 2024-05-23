import React, {useState, useEffect} from 'react';
 import "../index.css";
 import "../Assets/Signin.css"
import Logo from "../Assets/images/temp_logo.png"
import axios from 'axios';

function SignIn() {
    const[email, setEmail] = useState('');
    const[password, setPassword] = useState('');

    const logInUser = () => {
        if(email.length === 0 || password.length === 0){
            alert('Invalid email or password')
        }
        else{
            axios.post('http://localhost:5000/login',{
                email: email,
                password: password
            })
            .then(function(response) {
                console.log(response);
            })
            .catch(function(error) {
                console.log(error, 'error');
                if (error.response.status === 401){
                    alert("Invalid credentials")
                }
            })
        }
    }


    // useEffect(() => {
    //     fetch("/login").then(
    //         data => {
    //             setData(data)
    //             console.log(data)
    //         }
    //     )

    // }, [])
  return (
   <>
   <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          {/* <img
            className="mx-auto h-10 w-auto"
            src={Logo}
            alt="Your Company"
          /> */}
          <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight  text-white	text-900">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" action="#" method="POST">
            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-white text-900">
                Email address
              </label>
              <div className="mt-2">
                <input
                  onChange={(e) => setEmail(e.target.value)}
                  value={email}
                  placeholder='email'
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                //   required
                  className="block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-white text-900">
                  Password
                </label>
                <div className="text-sm">
                  <a href="#" className="font-semibold text-white-600 hover:text-white-500">
                    Forgot password?
                  </a>
                </div>
              </div>
              <div className="mt-2">
                <input
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                  placeholder='password'
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                //   required
                  className="block pl-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                onClick={logInUser}
                className="flex w-full justify-center rounded-md bg-king px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Sign in
              </button>
            </div>
          </form>

          <p className="mt-10 text-center text-sm text-black text-500">
            Not a member?{' '}
            <a href="#" className="font-semibold leading-6 text-white text-600 hover:text-indigo-500">
              Sign up
            </a>
          </p>
        </div>
      </div>
   </>
  )
}

export default SignIn