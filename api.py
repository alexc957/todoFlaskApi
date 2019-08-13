from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from flask_marshmallow import Marshmallow 
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SECRET_KEY']='secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+os.path.join(basedir,'vueAppDB.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma = Marshmallow(app) 


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in requests.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            print("")

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)   
    
# User schema 
class UserSchema(ma.Schema):
    class Meta:
        fields = ('public_id','name','password','admin') 

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True,strict=True)


@app.route('/user',methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result.data)

@app.route('/user/<public_id>',methods=['GET'])
def get_one_user(public_id):
    user =  User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"No user found"})
    return user_schema.jsonify(user)

@app.route('/user',methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data.get('password'),method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    name=data.get('name'),
                    password=hashed_password,
                    admin=False)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'new user Created'})

@app.route('/user/<public_id>',methods=['PUT'])
def promote_user(public_id):
    user =  User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"No user found"})
    user.admin = True
    db.session.commit()
    return jsonify({"message":"The user has been promoted"})

@app.route('/user/<public_id>',methods=['DELETE'])
def delete_user(public_id):
    user =  User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"No user found"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'user has been deleted'})
@app.route('/login')
def login():
    auth = request.authorization 
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login requiered"'})

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login requiered"'})
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'public_id': user.public_id,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'],algorithm='HS256')
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login requiered"'})

if __name__=="__main__":
    print("hola")
    app.run(debug=True)