
# YWCC307-Project

## Requirements
1. `pip install Flask`
2. `pip install Flask-SQLAlchemy`
3. `pip install psycopg2`

## Database Req 
Must have a local postgresql database set up. 
On app.py replace line 
`app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/dbname' `
with your database username, password, and database name

In order to initialize the database with some dummy data run a python shell and run the following:
```
from problem_model import db, Problem
db.create_all() 
problem1 = Problem(ptype='algebra', question='x+1=5', answer='4') 

problem2 = Problem(ptype='algebra', question='3*x+1=10', answer='3') 

problem3 = Problem(ptype='algebra', question='5*x=100', answer='20')

db.session.add(problem1)
db.session.add(problem2)
db.session.add(problem3)
db.session.commit()
```


## Run Application
1. Run command in terminal `python app.py`
2. Preview web page in browser
