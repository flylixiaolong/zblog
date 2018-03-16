"""
    flask application config file.
"""


class Config(object):
    """Base config"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost/blog"
