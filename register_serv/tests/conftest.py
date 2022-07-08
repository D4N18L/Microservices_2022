import pytest

from register_serv.application import create_app,db
from register_serv.application.models import Crownpass


@pytest.fixture(scope='session')
def flask_app():
    app = create_app()

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope='session')
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):

    user = Crownpass()
    user.username = 'johndoe'
    user.email = 'johndoe@gmail.com'
    user.first_name = 'John'
    user.last_name = 'Doe'
    user.password = 'password'

    db.session.add(user)
    db.session.commit()

    yield app_with_db

    db.session.delete(user)
    db.session.commit()
