from flask import Flask
from config import Config
from .site.routes import site

app = Flask(__name__)

app.register_blueprint(site)

app.config.from_object(Config)