import React from "react";

function CodeQuestions() {
  return (
    <div>
      <header>
        <h1>Code Questions</h1>
      </header>
      <div className="container">
        <div className="submission-box">
          <h3>
            Let us help you with your debugging today. Post your question here
          </h3>
          <form action="submit_question.php" method="post">
            <input
              type="text"
              name="title"
              placeholder="Question Title"
              required
            />
            <textarea
              name="content"
              rows="5"
              placeholder="Describe your question here..."
              required
            ></textarea>
            <input type="submit" value="Submit Question" />
          </form>
        </div>
        <div className="posts">
          {/* Example post 1 */}
          <div className="post">
            <h3>How to center a div?</h3>
            <p>
              Question description goes here. This is an example of a code
              question asked by a member For instance what is the best way to
              center a div? Been seeing this question in memes lately.
            </p>
            <div className="comments">
              <h4>Answers</h4>
              {/* Example comment 1 */}
              <div className="comment">
                <p>
                  <strong>User1:</strong> Answer to the question.
                </p>
              </div>
              <div className="comment-form">
                <input type="text" placeholder="Add an answer..." />
                <input type="submit" value="Post Answer" />
              </div>
            </div>
          </div>
          {/* Example post 2 */}
          <div className="post">
            <h3>Question Title 2</h3>
            <p>
              Another question description goes here. This is another example of
              a code question asked by a member.
            </p>
            <div className="comments">
              <h4>Answers</h4>
              {/* Example comment 2 */}
              <div className="comment">
                <p>
                  <strong>User2:</strong> Another answer to the question.
                </p>
              </div>
              <div className="comment-form">
                <input type="text" placeholder="Add an answer..." />
                <input type="submit" value="Post Answer" />
              </div>
            </div>
          </div>
          {/* Additional questions will be inserted here */}
        </div>
      </div>
    </div>
  );
}

export default CodeQuestions;
