from flask import Blueprint

display_api_blueprint = Blueprint('display_api', __name__)

from . import routes
