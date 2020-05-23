from flask import Flask
from flask_bootstrap import Bootstrap
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(APP_ROOT, 'static')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = STATIC_FOLDER

bootstrap = Bootstrap(app)

from app import routes

