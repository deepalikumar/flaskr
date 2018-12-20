import os
import tempfile
from datetime import datetime

import pytest
from flaskr import create_app
from flaskr.db import init_db, sql, User, Post
from werkzeug import generate_password_hash

def seed_test_data():
    for username, password in (('test', 'test'), ('other', 'other')):
        user = User(username=username,
            password=generate_password_hash(password))
        sql.session.add(user)
    
    created = datetime(2018, 1, 1, 0, 0, 0)
    post = Post(title='test title', body="test\nbody",
        author_id=1, created=created)
    sql.session.add(post)

    sql.session.commit()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///%s' % db_path,
    })

    with app.app_context():
        init_db()
        seed_test_data()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username="test", password="test"):
        return self._client.post(
        '/auth/login',
        data={'username': username, 'password': password}
        )
    def logout(self):
        return self._client.get('auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)