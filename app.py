import os
from random import randint
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort
#from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS 

#load_dotenv(find_dotenv())  # This is to load your env variables from .env

app = Flask(__name__)
#Must change this line in order to work with your local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pat:123abc@localhost/mathapp'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

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

def getUserbyName(inputUser):
    return db.session.query(problem_model.App_User).filter_by(username=inputUser).first()

def getUserbyID(inputID): 
    return db.session.query(problem_model.App_User).filter_by(id=inputID).first()

class User(Resource): 
    def get(self, user_ID): 
        user = getUserbyID(user_ID)
        imgprof = problem_model.Profile_Img.query.filter_by(id=user.profileImgID).first()
        
        userObj = {}
        userObj['name'] = user.username
        userObj['points'] = user.point  
        userObj['streak'] = user.streak
        userObj['attempts'] = user.attempt
        userObj['profileImgID'] = imgprof.img_url 

        return userObj

class Login(Resource): 
    def post(self):
        inputname = request.form['username']
        user = getUserbyName(inputname)
        if user:
            return{
                'userID':user.id, 
                'userName':user.username
            }
        
        abort(404, message="User {} doesn't exist".format(inputname))

class UserStreak(Resource): 
    def put(self, user_ID):
        try:
            new_streak = request.form['streak']
            user = getUserbyID(user_ID)
            if user: 
                user.streak = new_streak
                db.session.commit()
                return 200
        except: 
            abort(404, message="Input Error")

class UserPoint(Resource): 
    def put(self, user_ID): 
        try: 
            new_point = request.form['point']
            user = getUserbyID(user_ID)
            if user: 
                user.point = new_point
                db.session.commit()
                return 200
        except: 
            abort(404, message="Input Error")

class UserAttempts(Resource): 
    def put(self, user_ID): 
        try:
            new_attempts = request.form['attempt']
            user = getUserbyID(user_ID)
            if user: 
                user.attempt = new_attempts 
                db.session.commit()
                return 200
        except: 
            abort(404, message="Input Error")

        
    

api.add_resource(Problem, '/problem')
api.add_resource(Login, '/login')
api.add_resource(User, '/user/<string:user_ID>')
api.add_resource(UserStreak, '/user/<string:user_ID>/streak')
api.add_resource(UserPoint, '/user/<string:user_ID>/point')
api.add_resource(UserAttempts, '/user/<string:user_ID>/attempt')

if __name__ == '__main__': 
    app.run(
        debug=True
    )
