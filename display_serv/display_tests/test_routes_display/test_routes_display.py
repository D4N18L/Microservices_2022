from flask import url_for


def test_get_qr_code(app_with_db_display):
    response = app_with_db_display.get(url_for("display_api.get_qr_code"))
    assert response.status_code == 200

def test_create_qr_code(app_with_db_display):
    response = app_with_db_display.post(url_for("display_api.create_qr_code"),
                                json={
                                    'user_id': 1,
                                    'qr_code': 'qrcode'
                                }
                                )
    assert response.status_code == 200


def test_delete_qr_code(app_with_db_display):
    response = app_with_db_display.delete(url_for("display_api.delete_qr_code"),
                                json={
                                    'user_id': 1,
                                    'qr_code': 'qrcode'
                                }
                                )
    assert response.status_code == 200


def test_update_qr_code(app_with_db_display):
    response = app_with_db_display.put(url_for("display_api.update_qr_code"),
                                json={
                                    'user_id': 1,
                                    'qr_code': 'qrcode'
                                }
                                )
    assert response.status_code == 200




