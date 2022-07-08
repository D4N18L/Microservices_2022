from flask import Blueprint

print_api_blueprint = Blueprint('print_api', __name__)

from . import routes
