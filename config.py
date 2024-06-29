import os


class Config(object):
    DEBUG=True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


def LocalEnv():
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/canpay_db'
    return SQLALCHEMY_DATABASE_URI