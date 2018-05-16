import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'D_L_U_G_B_O_T'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True