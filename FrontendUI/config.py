import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = "OmBJumNGbRR-GTqyIVRcag"
    WTF_CSRF_SECRET_KEY = "VkRQAb4iBY8Fr--gyDEtwoIEUrgEz3KQssX1mNKD"

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False