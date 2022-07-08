from . import register_api_blueprint
from .. import db, login_manager
from ..models import Crownpass
from flask import request, jsonify, make_response, current_app, url_for
from flask_login import current_user, login_required, login_user, logout_user
from passlib.hash import sha256_crypt


@login_manager.user_loader
def load_user(id):
    return Crownpass.query.get(int(id))


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = Crownpass.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None


@register_api_blueprint.route('/get_users', methods=['GET'])  # localhost:5000/get_users
def get_users():
    data = []
    for user in Crownpass.query.all():
        data.append(user.convert_to_json())
    response = jsonify(data)
    return response


@register_api_blueprint.route('/save_image', methods=['POST'])  # localhost:5000/save_image
def save_image():
    profile_picture = request.files['profile_picture']
    img = Crownpass()
    img.profile_picture = profile_picture
    db.session.add(img)
    db.session.commit()
    return make_response(jsonify({'message': 'Image saved'}), 200)


@register_api_blueprint.route('/create_user', methods=['POST'])  # localhost:5000/create_user
def create_user():
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = sha256_crypt.hash(str(request.form['password']))
    address = request.form['address']
    phone = request.form['phone']

    user = Crownpass()
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.email = email
    user.password = password
    user.address = address
    user.phone = phone
    user.authenticated = True

    db.session.add(user)  # add user to database
    db.session.commit()  # commit changes to database

    response = jsonify({'message': 'User created successfully', 'user': user.convert_to_json()})

    return response


@register_api_blueprint.route('/login', methods=['POST'])  # localhost:5000/login
def login():
    username = request.form['username']
    user = Crownpass.query.filter_by(username=username).first()
    if user:
        if sha256_crypt.verify(str(request.form['password']), user.password):
            user.encrypt_api_key()
            db.session.commit()
            login_user(user)
            return make_response(jsonify({'message': 'User logged in successfully', 'user': user.convert_to_json(), 'api_key': user.api_key}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid password'}), 401)
    else:
        return make_response(jsonify({'message': 'Invalid username'}), 401)


@register_api_blueprint.route('/logout', methods=['POST'])  # localhost:5000/logout
def logout():
    if current_user.is_authenticated:
        logout_user()
        response = jsonify({'message': 'User logged out successfully'})
        return response
    else:
        response = jsonify({'message': 'User is not logged in'})
        return response


@register_api_blueprint.route('/user/<username>/exists', methods=['GET'])  # localhost:5000/user/<username>/exists
def username_exists(username):
    exist = Crownpass.query.filter_by(username=username).first()  # get user with username
    if exist:  # if user exists
        response = jsonify({'message': 'User exists'}), 200
    else:
        response = jsonify({'message': 'User does not exist'}), 404
    return response


@login_required
@register_api_blueprint.route('/<username>/active', methods=['GET'])  # localhost:5000/<username>/active
def username_active(username):
    item = Crownpass.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})  # if user exists
    else:
        response = jsonify({'message': 'User is not active'}, 404)  #
    return response


@login_required
@register_api_blueprint.route('/user', methods=['GET'])  # localhost:5000/user
def get_user():
    if current_user.is_authenticated:
        return make_response(jsonify({'user': current_user.convert_to_json()}))
    else:
        return make_response(jsonify({'message': 'User is not logged in'}), 401)


@login_required
@register_api_blueprint.route('/remove_user', methods=['DELETE'])  # localhost:5000/remove_user
def remove_user(username):
    user = Crownpass.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        response = jsonify({'message': 'User deleted successfully'})
        return response
    else:
        response = jsonify({'message': 'User does not exist'}, 404)
        return response


@register_api_blueprint.route('/user/remove_all', methods=['DELETE'])  # localhost:5000/user/remove_all
def remove_all_users():
    users = Crownpass.query.all()
    if users:
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'All users deleted successfully'}))
    else:
        return make_response(jsonify({'message': 'No users to delete'}), 404)
