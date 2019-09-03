from flaskTodoAPi import ma 
from flaskTodoAPi.models import Task

class UserSchema(ma.Schema):
    class Meta:
        fields = ('public_id','email','name','password','admin') 


class TagSchema(ma.Schema):
    class Meta:
        fields = ['name']

class TaskSchema(ma.ModelSchema):
    tags = ma.Nested(TagSchema, many= True)
    class Meta:
        model = Task