import React, {useState, useEffect} from 'react';
import "../index.css";


function SignIn() {
    const[data, setData] = useState([{}])

    useEffect(() => {
        fetch("/login").then(
            data => {
                setData(data)
                console.log(data)
            }
        )

    }, [])
  return (
    <div style={{backgroundColor: 'purple',
    height: 700}}>
        SIGNUP
    </div>
  )
}

export default SignIn