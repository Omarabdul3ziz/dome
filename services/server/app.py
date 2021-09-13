from flask import Flask
from flask_cors import CORS

import os 

from api import api
from auth import  github_blueprint, auth_blueprint, JWTManager
from model import DATABASE_URL


app = Flask(__name__)


CORS(app)

jwt = JWTManager(app)

SECRET_KEY = os.getenv("SECRET_KEY")

app.config['SECRET_KEY'] = SECRET_KEY

app.config["MONGO_URI"] = DATABASE_URL

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = SECRET_KEY  # Change this in your code!
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # to skip the missing token 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_COOKIE_DOMAIN'] = 'dome.vue'

api.init_app(app)

app.register_blueprint(github_blueprint, url_prefix='/login')
app.register_blueprint(auth_blueprint,  url_prefix='/auth')
