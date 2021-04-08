import os
<<<<<<< HEAD
import problem_model
from random import randint
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
#Must change this line in order to work with your local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123abc@localhost/mathapp'

api = Api(app)
db = SQLAlchemy(app)

class Problem(Resource): 
    def get(self): 
        num = problem_model.Problem.query.count() 
        randQuestion = randint(1, num) #Gets random question id

        probObj = problem_model.Problem.query.filter_by(id=randQuestion).first() 
        
        return {
            "id":probObj.id,
            "type":probObj.ptype,
            "question": probObj.question,
            "answer":probObj.answer
        }

class LeadBoard(Resource): 
    def get(self): 
        allUser = problem_model.App_User.query.all()
        part = {'users': []} 

        for user in allUser:
            userObj = {}
            userObj['name'] = user.username
            userObj['points'] = user.point
            part['users'].append(userObj) 
        
        return part

api.add_resource(Problem, '/problem')
api.add_resource(LeadBoard, '/users')
=======
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
>>>>>>> c315ca6fffa1de2ea30a7cae33b91afa3ee5408a

if __name__ == '__main__': 
    app.run(
        debug=True
    )
