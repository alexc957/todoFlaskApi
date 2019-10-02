from flaskTodoAPi import app, db
from flaskTodoAPi.models import User, Task
import json
import pytest

@pytest.fixture(scope='module')
def test_client():
    
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

def test_create_task(test_client):
    task_data = {
        "publicId" : "857597ad-e027-4fb5-a9c6-dcc74ac480c2",
        "tags": ["Javascript","Vue","Todo"],
        "title": "Test title",
        "description" : "Test description",
        "startDate": "2019-08-29",
        "dueDate": "2019-10-29",
        "status" : "Not Started"
    }
    response = test_client.post('/api/tasks/task',
                                data=json.dumps(task_data),
                                content_type='application/json')
    data = response.get_json()
    assert data.get('message') == 'Task created'
    assert not data.get('error')

def test_update_task(test_client):
    user = User.query.filter_by(email="prueba@gmail.com").first()
    last_task = user.tasks.pop()
    task_data_updated = {
        "id": last_task.id,
        "tags": ["Javascript","Vue","Todo", "VueJs" , "Django"],
        "title": "Test title",
        "description" : "Test description",
        "startDate": "2019-08-29",
        "dueDate": "2019-10-29",
        "status" : "Done"
    }

    response = test_client.put('/api/tasks/task',
                                data = json.dumps(task_data_updated),
                                content_type='application/json')
    data = response.get_json()
    assert data.get('message') == 'Task updated!'
    assert not data.get('error')



def test_create_task_with_invalid_public_id(test_client):
    task_data = {
        "publicId" : "857597ad-e02ddddddddd2",
        "tags": ["Javascript","Vue","Todo"],
        "title": "Test title",
        "description" : "Test description",
        "startDate": "2019-08-29",
        "dueDate": "2019-10-29",
        "status" : "Not Started"
    }
    response = test_client.post('/api/tasks/task',
                                data=json.dumps(task_data),
                                content_type='application/json')
    data = response.get_json()
    assert data.get('message') == 'User not found'
    assert data.get('error')

def test_get_all_tasks_by_user(test_client):
    public_id = '857597ad-e027-4fb5-a9c6-dcc74ac480c2'
    response = test_client.get('/api/tasks/task/'+public_id)
    data = response.get_json()
    assert data.get('tasks') is not None
    assert not data.get('error')

def test_get_all_tasks_by_unregistered_user(test_client):
    public_id = '8575sssssssss7-4fb5-a9c6-dcc74ac480c2'
    response = test_client.get('/api/tasks/task/'+public_id)
    data = response.get_json()
    assert data.get('message') == 'not user found'
    assert data.get('error')

def test_delete_task_by_id(test_client):
    user = User.query.filter_by(email="prueba@gmail.com").first()
    last_task = user.tasks.pop()

    response = test_client.delete('/api/tasks/task/'+str(last_task.id))
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('message') == "task deleted"
    assert not data.get('error')

