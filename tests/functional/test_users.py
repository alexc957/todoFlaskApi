from flaskTodoAPi import app, db
from flaskTodoAPi.models import User
import json
import pytest 

@pytest.fixture(scope='module')
def test_client():
    
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


def test_get_user_by_public_id(test_client):
    # this user already exist in the db 
    public_id = "857597ad-e027-4fb5-a9c6-dcc74ac480c2"
    response = test_client.get('/api/users/user/'+public_id)
    print("data? ")
    #with open('data.txt','+a') as f:
        #f.write(response.data)
    print(response.get_json())
    data= response.get_json()
    assert response.status_code == 200 
    assert not data.get('admin')
    assert data.get('email') == 'prueba@gmail.com'
    assert data.get('name') == 'prueba'
    assert data.get('password') != '12345678'

def test_get_user_that_does_not_exist(test_client):
    public_id = "857597a"
    response = test_client.get('/api/users/user/'+public_id)
    print("data? ")
    print(response.get_json())
    data= response.get_json()
    assert response.status_code == 200 
    assert data.get('message') == 'No user found'

def test_delete_user_that_exist(test_client):
    email = "usertest@mail.com"
    response = test_client.delete('/api/users/user/'+email)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('message') == 'user has been deleted'

def test_delete_user_that_does_not_exist(test_client):
    email = "mailthatnoexist@mail.com"
    response = test_client.delete('/api/users/user/'+email)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('message') == 'No user found'

    
def test_create_user(test_client):
    new_user = {
        "name" : "user test",
        "password" : 'password',
        "email" : "usertest@mail.com"
    }
    response = test_client.post('/api/users/user',
                                data=json.dumps(new_user),
                                content_type = 'application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('message') == 'new user Created'
    assert not data.get('error')
   
def test_login_with_credentials(test_client):
    credentials = {
        "email" : "usertest@mail.com",
        "password" : "password"
    }
    response = test_client.post('/api/users/login',
                                data= json.dumps(credentials),
                                content_type = 'application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert 'token' in data.keys()
    assert not data.get('error')
    assert 'public_id' in data.keys()

def test_login_with_no_email(test_client):
    credentials = {

        "password" : "password"
    }
    response = test_client.post('/api/users/login',
                                data= json.dumps(credentials),
                                content_type = 'application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('message') == 'Could no verify'
    assert data.get('error')

def test_login_with_bad_credentials(test_client):
    credentials = {
        "email" : "usertest@mail.com",        
        "password" : "invalid password"
    }
    response = test_client.post('/api/users/login',
                                data= json.dumps(credentials),
                                content_type = 'application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('message') == 'Bad credentials'
    assert data.get('error')

def test_promote_user_that_exist(test_client):
    email = 'usertest@mail.com'
    response = test_client.put('/api/users/user/'+email)
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('message') == 'The user has been promoted'

def test_promote_user_that_does_not_exist(test_client):
    email = 'this_email_does_not_exist@mail.com'
    response = test_client.put('/api/users/user/'+email)
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('message') == 'No user found'

def test_get_all_users(test_client):
    response = test_client.get('/api/users/user')
    data = response.get_json()
    assert response.status_code == 200
    assert data is not None