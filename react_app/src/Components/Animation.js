import React from 'react'
import {motion} from "framer-motion"
import "../Assets/Animation.css"
import Pic from "../Assets/images/sciene.png"
import Pic2 from "../Assets/images/python.png"
import Pic3 from "../Assets/images/linux.png"
import Pic4 from "../Assets/images/java.png"
import Pic5 from "../Assets/images/agile.png"
import Pic6 from "../Assets/images/ai.png"
import Pic7 from "../Assets/images/php.png"
import Pic8 from "../Assets/images/node.png"
import Pic9 from "../Assets/images/C++.png"
import Pic10 from "../Assets/images/ruby.png"
import Pic11 from "../Assets/images/sql.png"
import Pic12 from "../Assets/images/html.png"
import Pic13 from "../Assets/images/css.png"
import Pic14 from "../Assets/images/trello.png"






const images =[
    {src: Pic, alt:'react'},
    {src: Pic2, alt:'python'},
    {src: Pic3, alt:'linux'},
    {src: Pic4, alt:'java'},
    {src: Pic5, alt:'agile'},
    {src: Pic6, alt:'ai'},
    {src: Pic7, alt:'php'},
    {src: Pic8, alt:'node'},
    {src: Pic9, alt:'C++'},
    {src: Pic10, alt:'ruby'},
    {src: Pic11, alt:'sql'},
    {src: Pic12, alt:'ruby'},
    {src: Pic13, alt:'ruby'},
    {src: Pic14, alt:'ruby'},


]

function Animation() {
  return (
 
        <div className='animation'>
            

            <div className='square-container'>
                <div className='heading-container'>
                    <h1 className='heading-one'>Your home Your space Your zone</h1>
                    <h2 className='heading-two'>Share with us Your stories, worries and coding journeys! </h2>
                </div>
                <div className='square'>
                {images.map((image, index) => (
                    <motion.div
                    key={index + 1}
                    className='animated-square'
                    animate={{
                        rotate: [0, 360],
                        x:['100vw', '-200vw'],
                        // x: [0, 200, 200, 0, -200, -200, 0],
                    }}
                        initial= {{x: '100vw'}}
                    transition={{ repeat: Infinity, duration:11}}
                    >
                        <img src={image.src} alt={image.alt} width='90' height='90'/>
                    </motion.div>

                ))}
                </div>
              
                   
            </div>
        </div>

  )
}

export default Animation