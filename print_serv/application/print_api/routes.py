import os
from .. import db
from ..models import PrintedCode
from . import print_api_blueprint
from flask import request, jsonify, abort, make_response

from .api.Qrcode import Qrcode


@print_api_blueprint.route("/print", methods=["POST"])
def print_code():
    get_qrcode = Qrcode.check_qr_to_print()

    if not get_qrcode:
        return make_response(jsonify({'message': 'Unauthorized'}), 401)
    else:
        print_pass = PrintedCode.is_printed() is True # check if the qr code has been printed
        if print_pass:
            return make_response(jsonify({'message': 'Code can be printed'}), 200)

    # if get_qrcode is None:
    # return make_response(jsonify({"message": "No codes available"}), 401)
# else:
# print_pass = PrintedCode.query.filter_by(is_printed=False).first()  # Get the first code that is not printed
# print_pass.print()
# print_pass.unprint() # Unprinted the code after it has been printed to allow it to be printed again
# return jsonify({"message": "Code printed"})
