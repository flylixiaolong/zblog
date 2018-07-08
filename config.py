"""
    flask application config file.
"""


import os


class Config(object):
    """Base config"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x14\xf0I#\xde\x1fze*P\xc0\xa3|\x10\xf4\xa4\x05\x9b\xc7}\xa5\x0f\x12K'
