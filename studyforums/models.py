from studyforums import db, UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(5000))
    author = db.Column(db.String(20))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(5000))
    author = db.Column(db.String(20))
    q_id = db.Column(db.Integer)