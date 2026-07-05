import os

os.environ['FLASK_ENV'] = 'testing'

from app import create_app
from app.models import Question, db


def make_client():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app.test_client(), app


def test_create_question():
    client, app = make_client()
    resp = client.post('/questions/', json={'text': 'How are you?'})

    assert resp.status_code == 201
    data = resp.get_json()
    assert data['text'] == 'How are you?'
    assert 'id' in data


def test_create_question_with_spaces():
    client, app = make_client()
    resp = client.post('/questions/', json={'text': '   How are you, BRO?   '})

    assert resp.status_code == 201
    data = resp.get_json()
    assert data['text'] == 'How are you, BRO?'
    assert 'id' in data


def test_list_questions():
    client, app = make_client()

    client.post('/questions/', json={'text': 'Question 1'})
    client.post('/questions/', json={'text': 'Question 2'})

    resp = client.get('/questions/')
    assert resp.status_code == 200
    data = resp.get_json()

    assert data['count'] == 2
    assert len(data['items']) == 2
