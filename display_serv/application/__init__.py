import config
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    environment_configuration = os.environ.get('CONFIGURATION_SETUP')
    app.config.from_object(environment_configuration)
    app.config.update(QR_CODE_LOCATION=os.path.join(dir_path, "qr_codes"))  # qr_codes is the path to the qr code

    db.init_app(app)

    with app.app_context():
        from .display_api import display_api_blueprint
        app.register_blueprint(display_api_blueprint)
        return app
