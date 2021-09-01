from flask import Flask
from flask_cors import CORS

from model import db
from api import api
from auth import login_blueprint, github_blueprint, login_manager


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret'


######## Db url and path
# MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
# MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
# DATABASE_URL = f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongo:27017'

DATABASE_URL = 'mongodb://localhost:27017'
app.config["MONGOALCHEMY_CONNECTION_STRING"] = DATABASE_URL
app.config["MONGOALCHEMY_DATABASE"] = 'tasksDb'

db.init_app(app)
login_manager.init_app(app)

api.init_app(app)
app.register_blueprint(login_blueprint)
app.register_blueprint(github_blueprint, url_prefix='/login')

