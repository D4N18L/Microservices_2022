import config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    environment_configuration = os.environ.get('CONFIGURATION_SETUP')
    app.config.from_object(environment_configuration)
    app.config.update(PRINTED_CODE_LOCATION=os.path.join(dir_path, "printed_codes")) # printed_codes is the path to the printed code

    db.init_app(app)

    with app.app_context():
        return app


