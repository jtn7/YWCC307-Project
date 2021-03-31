import os
import problem_model
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Must change this line in order to work with your local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/dbname'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    """ Returns root endpoint HTML """

    # sample problem 
    prob = "5+3"

    return render_template(
        "index.html",
        problem = prob,
    )

@app.route('/submit/<user_text>')
def give_user_feedback(user_text):
    '''
        This function takes the answer submited by user and 
        returns the feedback and correct answer
    '''

    '''
    Any example of getting a problem from database with id=1 

    probObj = problem_model.Problem.query.filter_by(id=1).first()
    print(probObj.question)
    print(probObj.answer)

    '''

    
    user_ans = int(user_text)
    
    # TODO get the correct answer from database
    # sample answer
    correct_ans = 8
    
    if user_ans == correct_ans:
        feed = "Correct Answer"
    else:
        feed = "Wrong Answer"

    return {
        'answer': correct_ans,
        'feedack': feed
    }

if __name__ == '__main__': 
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
