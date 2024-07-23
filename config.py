import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key'


# class Config:
#     SECRET_KEY = 'key'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class DevelopmentConfig(Config):
#     DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False
