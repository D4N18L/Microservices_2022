import pytest

from print_serv.application import create_app,db
from print_serv.application.models import PrintedCode


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

    print = PrintedCode()
    print.id = 1
    print.is_printed = False

    db.session.add(print)
    db.session.commit()

    yield app_with_db

    db.session.delete(print)
    db.session.commit()
