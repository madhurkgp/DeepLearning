from flask import Flask
import os

app = Flask(__name__)

# Use os.environ.get to avoid KeyError and default to production if not set
env = os.environ.get("FLASK_ENV", "production")

if env == "development":
    app.config.from_object("config.DevelopmentConfig")
elif env == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.ProductionConfig")

from app import views
