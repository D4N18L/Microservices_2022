from flask import url_for


def test_print_code(app_with_db):
    response = app_with_db.post(url_for("print_api.print_code"),
                                json={
                                'id': 1,
                                'is_printed': False
                                })
    assert response.status_code == 200
