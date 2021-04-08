from app import db

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

    def __repr__(self): 
        return '<User %r>' % self.username