import React, { useState } from "react";
import "./index.css";

function LongestCodingStreaks() {
  const [codedToday, setCodedToday] = useState(false); // State to track whether the member has coded today
  const [codeHours, setCodeHours] = useState(0); // State to track the number of hours coded today

  const handleToggle = () => {
    setCodedToday(!codedToday); // Toggle the codedToday state
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you can handle the submission of code of the day
    console.log("Code submitted:", codeHours, "hours");
  };

  return (
    <div className="longest-streaks-container">
      <div className="coding-streaks-section">
        <h2>Longest Coding Streaks</h2>
        <ul>
          <li>1. John Doe - 365 days</li>
          <li>2. Jane Smith - 300 days</li>
          {/* Add more streaks as needed */}
        </ul>
      </div>
      <div className="coding-today-section">
        <h2>Did you code today?</h2>
        <label>
          <input
            type="checkbox"
            checked={codedToday}
            onChange={handleToggle}
          />
          Yes, I coded today
        </label>
        {codedToday && (
          <form onSubmit={handleSubmit}>
            <label>
              How many hours did you code today?
              <input
                type="number"
                value={codeHours}
                onChange={(e) => setCodeHours(e.target.value)}
                required
              />
            </label>
            <button type="submit">Submit</button>
          </form>
        )}
      </div>
      <div className="code-post-section">
        <h2>Post Your Code of the Day</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Number of Hours Coded:
            <input
              type="number"
              value={codeHours}
              onChange={(e) => setCodeHours(e.target.value)}
              required
            />
          </label>
          <textarea
            placeholder="Write your code here..."
            required
          ></textarea>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default LongestCodingStreaks;
