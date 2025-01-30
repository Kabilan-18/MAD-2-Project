from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_app.workers import celery_init_app
from flask_caching import Cache
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = '49b2d4bd73187a7927e435ba1af160b4'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["JWT_SECRET_KEY"] = '943252379fsa23894afsafgyafka'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=5)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = '6379'


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

cache = Cache(app)

celery = celery_init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})

from flask_app import api
from flask_app import routes