import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = "cxNmGcPBK8PdRA5-9JU0RQ"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = "AHHafC6CBJVd72erFKhgfslUmlcDRiGvxgP3gJdL"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bigdata2022:trick123@localhost:3306/print_microservice"
    SQLALCHEMY_ECHO = True
    TESTING = True


class Production(Config):
    pass
