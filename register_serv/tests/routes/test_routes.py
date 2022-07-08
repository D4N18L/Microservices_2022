from flask import url_for


def test_no_user(app_with_db):
    response = app_with_db.post(url_for("register_api.login"),
                                json={
                                    'username': 'johndoe',
                                    'password': 'password'
                                }
                                )

    assert response.status_code == 200


def test_user_login(app_with_db):
    response = app_with_db.post(url_for("register_api.login"),
                                json={
                                    'username': 'johndoe',
                                    'password': 'password'
                                }
                                )

    assert response.status_code == 200

    #data = response.get_json()
    #assert data['message'] == "User logged in successfully"


def test_user_login_wrong_password(app_with_db):

    response = app_with_db.post(url_for("register_api.login"),
                                json={
                                    'username': 'johndoe',
                                    'password': 'wrongpassword'
                                }
                                )

    assert response.status_code == 200

    #data = response.get_json()
    #assert data['message'] == "User logged in successfully"


def test_user_login_wrong_username(app_with_db):

        response = app_with_db.post(url_for("register_api.login"),
                                    json={
                                        'username': 'wrongusername',
                                        'password': 'password'
                                    }
                                    )

        assert response.status_code == 200

        #data = response.get_json()
        #assert data['message'] == "User logged in successfully"



def test_user_login_wrong_username_and_password(app_with_db):

            response = app_with_db.post(url_for("register_api.login"),
                                        json={
                                            'username': 'wrongusername',
                                            'password': 'wrongpassword'
                                        }
                                        )

            assert response.status_code == 200

            #data = response.get_json()
            #assert data['message'] == "User logged in successfully"


def test_user_login_wrong_username_and_password_2(app_with_db):

                    response = app_with_db.post(url_for("register_api.login"),
                                                json={
                                                    'username': 'wrongusername',
                                                    'password': 'wrongpassword'
                                                }
                                                )

                    assert response.status_code == 200

                    #data = response.get_json()
                    #assert data['message'] == "User logged in successfully"


def test_create_user(app_with_db):
    response = app_with_db.post(url_for("register_api.create_user"),
                                json={
                                    'username': 'dandoe',
                                    'email': 'dandoe@gmail.com',
                                    'first_name': 'Dan',
                                    'last_name': 'Doe',
                                    'password': 'password'
                                }
                                )

    assert response.status_code == 200











