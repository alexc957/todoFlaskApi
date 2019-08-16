from flaskTodoAPi import app, ma, db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime
from flask import jsonify, request, make_response
from flaskTodoAPi.models import User


class UserSchema(ma.Schema):
    class Meta:
        fields = ('public_id','email','name','password','admin') 

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True,strict=True)


@app.route('/api/user',methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result.data)

@app.route('/api/user/<public_id>',methods=['GET'])


def get_one_user(public_id):
    user =  User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"No user found"})
    return user_schema.jsonify(user)

@app.route('/api/user',methods=['POST'])

def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data.get('password'),method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    name=data.get('name'),
                    email = data.get('email'),
                    password=hashed_password,
                    admin=False)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'new user Created'})

@app.route('/api/user/<public_id>',methods=['PUT'])

def promote_user(public_id):
    user =  User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"No user found"})
    user.admin = True
    db.session.commit()
    return jsonify({"message":"The user has been promoted"})

@app.route('/api/user/<public_id>',methods=['DELETE'])

def delete_user(public_id):
    user =  User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message":"No user found"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'user has been deleted'})

@app.route('/api/login',methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message":"Could no verify", "error":"true"})

    user = User.query.filter_by(email=data.get('email')).first()
    if not user:           
        return jsonify({"message":"Bad credentials", "error":"true"})
    if check_password_hash(user.password,data.get('password')):
        token = jwt.encode({'public_id': user.public_id,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'],algorithm='HS256')
        return jsonify({'token' : token.decode('UTF-8')})
    return jsonify({"message":"Bad credentials", "error":"true"})