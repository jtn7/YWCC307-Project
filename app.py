import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import random

load_dotenv(find_dotenv())  # This is to load your env variables from .env

app = Flask(__name__)
#Must change this line in order to work with your local database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


import problem_model
db.create_all()

@app.route('/problem/')
def new_problem():
    ''' 
        this function provies a problem to the user upon request
    '''
    
    # get a random question from database
    totalProblems = problem_model.Problem.query.count()
    randomProblemID = random.randint(1, totalProblems)
    
    probObj = problem_model.Problem.query.filter_by(id=randomProblemID).first()

    quesId = randomProblemID
    typeOfQues = probObj.ptype
    ques = probObj.question
    ans = probObj.answer

    return {
        "id":quesId,
        "type":typeOfQues,
        "question": ques,
        "answer":ans
    }

if __name__ == '__main__': 
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
