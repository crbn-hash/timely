class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='sqlite:///database.db'
    SQLALCHEMY_ECHO=True
    SECRET_KEY ='mysecret' #random generated string