from unittest import mock

from flask import url_for


def fake_session(query):
    class FakeQuery:
        def all(self):
            return [{'id': 1, 'username': 'dandoe', 'email': 'dandoe@gmail.com',
                     'first_name': 'Dan', 'last_name': 'Doe', 'password': 'password'}]

    return FakeQuery()


@mock.patch("register_serv.application.db.session.scalars", new=lambda query: fake_session(query))
def test_get_users(flask_app):

    response = flask_app.get(url_for("register_api.get_users"))

    assert response.status_code == 200

    #data = response.get_json()
    #assert len(data) == 1


def test_get_all_users(flask_app):

    with mock.patch("register_serv.application.db.session.scalars") as mocked_session:
        mocked_session.return_value = fake_session(None)

        response = flask_app.get(url_for("register_api.get_users"))

        assert response.status_code == 200


def test_remove_user(flask_app):

    with mock.patch("register_serv.application.db.session.scalars") as mocked_session:
        mocked_session.return_value = fake_session(None)

        response = flask_app.delete(url_for("register_api.remove_user", user_id=1))

        assert response.status_code == 200


def test_remove_all_users(flask_app):

    with mock.patch("register_serv.application.db.session.scalars") as mocked_session:
        mocked_session.return_value = fake_session(None)

        response = flask_app.delete(url_for("register_api.remove_all_users"))

        assert response.status_code == 200






