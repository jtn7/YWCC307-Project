import os
from random import randint
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS 

load_dotenv(find_dotenv())  # This is to load your env variables from .env

app = Flask(__name__)
#Must change this line in order to work with your local database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pat:password@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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

def addNewUser(name, imgId):
    ''' helper function to add a new user to database'''
    user = getUserbyName(name)
    if not user:
        new_user = problem_model.App_User(username=name, point=0, attempt=0, streak=0, profileImgID=imgId)
        db.session.add(new_user)
        db.session.commit()
        
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
        
class AllUsers(Resource):
    def get(self):
        ''' get all users from database in descending order (according to points) '''
        all_user = problem_model.App_User.query.order_by(problem_model.App_User.point.desc()).all()
        users = []
        for person in all_user:
            d = {
                "username": person.username,
                "point": person.point,
                "attempt": person.attempt,
                "streak": person.streak,
                "imageID": person.profileImgID
            }
            users.append(d)
        return users

class Login(Resource): 
    def post(self):
        request_data = request.get_json()
        username = request_data["username"]
        imgId = request_data["profileImgID"]
        addNewUser(username, imgId)
        user = getUserbyName(username)
        
        return{
            'userID':user.id, 
        }

class UserStreak(Resource): 
    def put(self, user_ID):
        try:
            request_data = request.get_json()
            new_streak = request_dat['streak']
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
            request_data = request.get_json()
            new_point = request_data['point']
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
            request_data = request.get_json()
            new_attempts = request_data['attempt']
            user = getUserbyID(user_ID)
            if user: 
                user.attempt = new_attempts 
                db.session.commit()
                return 200
        except: 
            abort(404, message="Input Error")

        
    

api.add_resource(Problem, '/problem')
api.add_resource(Login, '/login')
api.add_resource(AllUsers, '/allusers')
api.add_resource(User, '/user/<string:user_ID>')
api.add_resource(UserStreak, '/user/<string:user_ID>/streak')
api.add_resource(UserPoint, '/user/<string:user_ID>/point')
api.add_resource(UserAttempts, '/user/<string:user_ID>/attempt')

if __name__ == '__main__': 
    app.run(
        port = int(os.getenv('PORT', 8080)),
        #host = os.getenv("IP", '0.0.0.0'),
        #debug  = True
    )
