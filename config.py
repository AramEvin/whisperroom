import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY            = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///whisperroom.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MESSAGE_HISTORY_LIMIT = 50
    MAX_MESSAGE_LENGTH    = 500
    MAX_ROOM_NAME_LENGTH  = 32
    ADMIN_PASSWORD        = os.environ.get('ADMIN_PASSWORD', 'admin1234')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
