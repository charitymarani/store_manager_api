"""
Imports
"""
'''instance/config.py'''


class Config(object):
    '''parent config file'''
    DEBUG = True
    SECRET_KEY = 'this is not a secret'


class Development(Config):
    '''Configurations for development'''
    Debug = True


class Testing(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    Debug = True


app_config = {
    'development': Development,
    'testing': Testing
}
