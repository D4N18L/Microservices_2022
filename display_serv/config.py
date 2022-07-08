import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = '31129c6303f7e935245f07'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bigdata2022:trick123@host.docker.internal:3306/display_microservice"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bigdata2022:trick123@localhost:3306/display_microservice"
    SQLALCHEMY_ECHO = True
    TESTING = False


class ProductionConfig(Config):
    pass
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bigdata2022:trick123@display-db:3306/display_microservice"
    SQLALCHEMY_ECHO = False
