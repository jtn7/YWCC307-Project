from problem_model import db, Problem
db.create_all() 
problem1 = Problem(ptype='algebra', question='x+1=5', answer='4') 

problem2 = Problem(ptype='algebra', question='3*x+1=10', answer='3') 

problem3 = Problem(ptype='algebra', question='5*x=100', answer='20')

db.session.add(problem1)
db.session.add(problem2)
db.session.add(problem3)
db.session.commit()