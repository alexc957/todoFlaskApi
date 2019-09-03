from flaskTodoAPi.models import User, Tag, Task 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import pytest

unique_user_id = uuid.uuid4()


@pytest.fixture(scope='module')
def new_user():
    hashed_password = generate_password_hash('password',method='sha256')

    new_user = User(public_id=str(unique_user_id),
                    name='user Test',
                    email = 'user@test.com',
                    password=hashed_password,
                    admin=False)
    return new_user


def test_new_user(new_user):
    assert new_user.public_id == str(unique_user_id)
    assert new_user.name == 'user Test'
    assert new_user.email == 'user@test.com'
    assert new_user.password != 'password'
    assert not new_user.admin

@pytest.fixture(scope='module')
def new_tag():
    return Tag(name='Test Tag')

def test_new_tag(new_tag):
    assert new_tag.name == 'Test Tag'

@pytest.fixture(scope='module')
def new_task():
    return Task(
        title='title',
        text='text',
        start_date = datetime.utcnow(),
        due_date = datetime.utcnow(),
        status = 'Not Started' 
    )

def test_new_task(new_task):
    assert new_task.title == 'title'
    assert new_task.text == 'text'
    assert new_task.start_date.strftime('%x') == datetime.utcnow().strftime('%x')
    assert new_task.status == 'Not Started'