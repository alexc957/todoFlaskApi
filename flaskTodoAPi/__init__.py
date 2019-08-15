from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os 
from flask_marshmallow import Marshmallow 

from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources='/api/*')
basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SECRET_KEY']='secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+os.path.join(basedir,'vueAppDB.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma = Marshmallow(app) 

from flaskTodoAPi import routes