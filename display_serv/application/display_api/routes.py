from flask import jsonify, request, make_response, current_app

from . import display_api_blueprint
from ..models import DisplayQrCode
from .api.Holder import Holder
from .. import db
import qrcode
from PIL import Image

"""
items = []

for item in DisplayQrCode.query.all():
    # get the most recent qr code
    items.append(item.convert_to_json())
return make_response(jsonify({'qr_code': items}))
"""

"""
if len(DisplayQrCode.query.all()) == 1:
    return jsonify(DisplayQrCode.query.first().convert_to_json())
# if there are more than one qr code in the database, return the most recent one
elif len(DisplayQrCode.query.all()) > 1:
    return jsonify(
        DisplayQrCode.query.order_by(DisplayQrCode.id.desc()).first().convert_to_json())  # get the most recent qr code
else:
    return make_response(jsonify({"message": "No codes available"}), 401)
"""


@display_api_blueprint.route('/get_qr_code', methods=['GET'])  # localhost:5001/get_qr_code
def get_qr_code():
    """
    Get the qr code
    :return: qr code
    """
    # qrcode = DisplayQrCode.query.all()
    qrcodes = DisplayQrCode.query.filter_by(user_id=request.headers.get('Authorization')).all()

    if len(qrcodes) == 1:
        return jsonify(qrcodes[0].convert_to_json())  # get the most recent qr code
    elif len(qrcodes) > 1:
        return jsonify(qrcodes[-1].convert_to_json())  # get the most recent qr code
    else:
        return make_response(jsonify({"message": "No codes available"}), 401)


@display_api_blueprint.route('/create_qr_code', methods=['POST'])  # localhost:5001/create_qr_code
def create_qr_code():
    api_key = request.headers.get('Authorization')
    # api_key = "$5$rounds=535000$.i3EfLWHGpAp1h4L$ieFLKJ/ZvO5iemyhzj8RCN07zVIrY7yMXbxhd1M3C.0"
    response = Holder.get_holder(api_key)

    if not response:
        return make_response(jsonify({'message': 'Unauthorized'}), 401)
    user = response['user']  # get the user from the database
    user_id = user['id']  # get the user id
    username = user['username']  # get the username from the database
    existing_qr_code = DisplayQrCode.query.filter_by(user_id=user_id,
                                                     is_active=True).first()  # get the qr code if it exists

    if existing_qr_code is None:
        existing_qr_code = DisplayQrCode()
        qr = qrcode.make(str(username))
        type(qr)
        qr_location = current_app.config['QR_CODE_LOCATION'] + str(user_id) + '.png'

        qr.save(qr_location)
        existing_qr_code.is_active = True
        existing_qr_code.user_id = user_id
        existing_qr_code.qr_code = qr_location  # qr_location is the path to the qr code
        db.session.add(existing_qr_code)
        db.session.commit()
        return make_response(jsonify({'message': 'Qr code created'}), 201)
    else:
        return make_response(jsonify({'message': 'Qr code already exists'}), 200)


@display_api_blueprint.route('/delete_qr_code', methods=['DELETE'])  # localhost:5001/delete_qr_code
def delete_qr_code():
    api_key = request.headers.get('Authorization')
    response = Holder.get_holder(api_key)

    if not response:
        return make_response(jsonify({'message': 'Unauthorized'}), 401)
    user = response['user']
    user_id = user['id']
    existing_qr_code = DisplayQrCode.query.filter_by(user_id=user_id, is_active=True).first()

    if existing_qr_code is None:
        return make_response(jsonify({'message': 'Qr code does not exist'}), 200)
    else:
        existing_qr_code.delete()
        db.session.commit()
        return make_response(jsonify({'message': 'Qr code deleted'}), 200)


@display_api_blueprint.route('/update_qr_code', methods=['PUT'])  # localhost:5001/update_qr_code
def update_qr_code():
    api_key = request.headers.get('Authorization')
    response = Holder.get_holder(api_key)

    if not response:
        return make_response(jsonify({'message': 'Unauthorized'}), 401)
    user = response['user']  # user is a dictionary
    user_id = user['id']  # user_id is an integer
    existing_qr_code = DisplayQrCode.query.filter_by(user_id=user_id, is_active=True).first()

    if existing_qr_code is None:
        return make_response(jsonify({'message': 'Qr code does not exist'}), 200)
    else:
        existing_qr_code.update(user_id)
        db.session.commit()
        return make_response(jsonify({'message': 'Qr code updated'}), 200)
