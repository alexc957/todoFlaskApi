from flaskTodoAPi import db
from flask import Blueprint, request, jsonify
import datetime
from flaskTodoAPi.models import User, Task, Tag
from flaskTodoAPi.schemas import TaskSchema

task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(many=True,strict=True)
tasks = Blueprint('tasks',__name__)

def get_tags_as_list_of_objects(tags_names):
    tags_objects = []
    for tag_name in tags_names:
        tag_db = Tag.query.filter_by(name=tag_name).first()
        if not tag_db:
            tag_db = Tag(name=tag_name)
        tags_objects.append(tag_db)
    return tags_objects


@tasks.route('/api/tasks/task',methods=['POST'])
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
        return jsonify({'message': 'User not found','error':True})
    task = Task(title=title,text=text,start_date=start_date,due_date=due_date,status=status)
    user.tasks.append(task)

    tags_objects = get_tags_as_list_of_objects(tags)
 
    for tag in tags_objects:
        task.tags.append(tag)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created','error':False})


@tasks.route('/api/tasks/task/<public_id>',methods=['GET'])
def get_tasks(public_id):

    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({
            "message" : "not user found",
            "error" : True
        })
    result = tasks_schema.dump(user.tasks)
    return jsonify({'tasks': result.data, 'error' : False})


@tasks.route('/api/tasks/task/<id>',methods= ['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=id).first()
    print(task)
    if not task:
        return jsonify({"message":"task not found", "error": True})
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message":"task deleted", "error": False})



