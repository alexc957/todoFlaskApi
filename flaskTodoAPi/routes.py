from flaskTodoAPi import app, ma, db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime
from flask import jsonify, request, make_response
from flaskTodoAPi.models import User,Task, Tag


class UserSchema(ma.Schema):
    class Meta:
        fields = ('public_id','email','name','password','admin') 

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True,strict=True)


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('title','text','start_time','due_date','complete')
task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(many=True,strict=True)

class TagSchema(ma.Schema):
    class Meta:
        fields = ['name']

tags_schema = TagSchema(many=True,strict=True)

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
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        return jsonify({'message':'Email already taken','error': True})
    hashed_password = generate_password_hash(data.get('password'),method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    name=data.get('name'),
                    email = data.get('email'),
                    password=hashed_password,
                    admin=False)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'new user Created','error': False}) 

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

@app.route('/api/verifyToken', methods= ['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    try:
        decoded = jwt.decode(token,app.config['SECRET_KEY'],algorithm='HS256')
        user = User.query.filter_by(public_id=decoded.get('public_id')).first()
        if not user:
            return jsonify({'tokenValid': False})
        return jsonify({'tokenValid':True})
    except jwt.ExpiredSignatureError:
        return jsonify({'tokenValid': False})
    #return jsonify({'tokenValid': False})

def get_tags_as_list_of_objects(tags_names):
    tags_objects = []
    for tag_name in tags_names:
        tag_db = Tag.query.filter_by(name=tag_name).first()
        if not tag_db:
            tag_db = Tag(name=tag_name)
        tags_objects.append(tag_db)
    return tags_objects


#tasks
@app.route('/api/task',methods=['POST'])
def create_task():
    data = request.get_json()
    public_id = data.get('publicId')
    tags = data.get('tags')
    title= data.get('title')
    text = data.get('description')
    start_date = data.get('startDate').split('-')
    due_date = data.get('dueDate').split('-')
    status = data.get('status')

    start_date = datetime.datetime(int(start_date[0]),int(start_date[1]),int(start_date[2]))
    due_date = datetime.datetime(int(due_date[0]),int(due_date[1]),int(due_date[2]))
        
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'Message': 'User not found','error':True})
    task = Task(title=title,text=text,start_date=start_date,due_date=due_date,status=status)
    user.tasks.append(task)

    tags_objects = get_tags_as_list_of_objects(tags)
    print(tags_objects)
    for tag in tags_objects:
        task.tags.append(tag)
    db.session.add(task)
    db.session.commit()
    return jsonify({'Message': 'Task created','error':False})


# tags 
@app.route('/api/tag',methods=['GET'])
def get_tags():
    all_tags = Tag.query.all()
    result = tags_schema.dump(all_tags)
    return jsonify(result.data)




@app.route('/api/login',methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message":"Could no verify", "error":True})

    user = User.query.filter_by(email=data.get('email')).first()
    if not user:           
        return jsonify({"message":"Bad credentials", "error":True})

    if check_password_hash(user.password,data.get('password')):
        token = jwt.encode({'public_id': user.public_id,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'],algorithm='HS256')
        return jsonify({'token' : token.decode('UTF-8'),'error': False, 'public_id': user.public_id})

    return jsonify({"message":"Bad credentials", "error":True})

## 