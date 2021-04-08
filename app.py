import os
from random import randint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your env variables from .env

app = Flask(__name__)
#Must change this line in order to work with your local database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)


import problem_model
db.create_all()

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

if __name__ == '__main__': 
    app.run(
        debug=True
    )
