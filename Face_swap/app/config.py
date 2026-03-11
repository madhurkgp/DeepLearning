class Config(object):
    SECRET_KEY = 'face_swap_app_2024'
    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class DevelopmentConfig(Config):
    DEBUG = True
