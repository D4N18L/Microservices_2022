
from flask import Blueprint

register_api_blueprint = Blueprint('register_api', __name__)

from . import routes