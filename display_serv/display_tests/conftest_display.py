import pytest
from display_serv.application import create_app_display, db
from display_serv.application.models import DisplayQrCode


@pytest.fixture(scope='session')
def flask_app_display():
    app = create_app_display()

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope='session')
def app_with_db_display(flask_app_display):
    db.create_all()

    yield flask_app_display

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data_display(app_with_db_display):
    qrcode = DisplayQrCode()
    qrcode.id = 1
    qrcode.user_id = 1
    qrcode.qr_code = 'qrcode'
    qrcode.is_active = True

    db.session.add(qrcode)
    db.session.commit()

    yield app_with_db_display

    db.session.delete(qrcode)
    db.session.commit()
