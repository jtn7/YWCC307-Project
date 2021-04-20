import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Must change this line in order to work with your local database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pat:password@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Problem(db.Model): 
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True)
    ptype = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.String(20), nullable=False)

    def __repr__(self): 
        return '<Problem %r>' % self.question
    

class App_User(db.Model): 
    __tablename__ = 'app_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    attempt = db.Column(db.Integer, nullable=False)
    streak = db.Column(db.Integer, nullable=False)
    profileImgID = db.Column(db.Integer, db.ForeignKey('profile_img.id'))

    def __repr__(self): 
        return '<User %r>' % self.username


class Profile_Img(db.Model):
    __tablename__ = 'profile_img'

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable = False) 
    