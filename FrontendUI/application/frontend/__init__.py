from flask import Blueprint

FE_blueprint = Blueprint('FE', __name__)

from . import routes
