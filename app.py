import os
import problem_model
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Must change this line in order to work with your local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/dbname'
db = SQLAlchemy(app)

@app.route('/problem/')
def new_problem():
    ''' 
        this function provies a problem to the user upon request
    '''
    
    # TODO get a random question from database
    # getting question from darabase with id = 1
    probObj = problem_model.Problem.query.filter_by(id=1).first()

    quesId = 1
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
