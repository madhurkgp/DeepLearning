class Config(object):

    SECRET_KEY = 'bird_species_app_secret_key_2024'

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class DevelopmentConfig(Config):
    DEBUG = True
