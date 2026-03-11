class Config(object):

    SECRET_KEY = 'vehicle_detection_app'

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class DevelopmentConfig(Config):
    DEBUG = True
