from flaskTodoAPi.models import User, Task, Tag
User.query.all()
user = User.query.all()[0]
user
from datetime import datetime
task = Task(title='tas',text='ds',due_date=datetime.utcnow(),status='done')
user.tasks.append(task)
tag1 = Tag(name='todo')
tag2 = Tag(name='Vue')
task.tags.append(tag1)
task.tags.append(tag2)
task.tags
from flaskTodoAPi import db
db.session.add(task)
db.session.commit()
%history -f example.py
