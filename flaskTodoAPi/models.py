from flaskTodoAPi import db, app 
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(30))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(30))
    text = db.Column(db.String(100))
    start_date = db.Column(db.DateTime,default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(30),default='Not Started')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) 
    user = db.relationship('User', backref = db.backref('tasks',lazy=True))
    
