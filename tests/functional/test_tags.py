from flaskTodoAPi import app, db
from flaskTodoAPi.models import Tag
import json
import pytest

@pytest.fixture(scope='module')
def test_client():
    
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

def test_get_tags(test_client):
    response = test_client.get('/api/tags/tag')
    data = response.get_json()
    assert response.status_code == 200
    assert data is not None
