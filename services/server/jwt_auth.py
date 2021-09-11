from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, g, jsonify, make_response
from pymongo import MongoClient
from functools import wraps
from flask_dance.contrib.github import make_github_blueprint, github
from werkzeug.wrappers import response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, unset_jwt_cookies, set_access_cookies
import os
from flask_cors import CORS



GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

app = Flask(__name__)

CORS(app)

jwt = JWTManager(app)


client = MongoClient('mongodb://localhost:27017/')
db = client['dome2']
users = db['users']
tasks = db['tasks']

app.config['SECRET_KEY'] = 'secret'

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )
app.register_blueprint(github_blueprint, url_prefix="/login")

@auth_bp.route('/github')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')
    if account_info.ok:
        username = account_info.json()['login']

    # fetch user from db
    user = users.find_one({'username': username})

    # or create new one
    if user is None:
        user = {'username': username,
                'password': "",
                'admin': False}

        users.insert(user)
        
    # create and respond with token
    access_token = create_access_token(identity=username)
    
    # default set cookie
    response = jsonify(access_token=access_token)
    set_access_cookies(response, access_token)

    # my custome set
    # response = make_response(redirect(url_for("index")))
    # response.set_cookie('access_token_cookie', access_token)
    return response


@auth_bp.route('/register', methods=['POST'])
def register():
    # getting criedentials from BODY
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # getting criedentials from HEADER
    # auth = request.authorization
    # username = auth.username
    # password = auth.password

    # creating new user
    user = {'username': username,
            'password': password,
            'admin': False}
    users.insert(user)

    # create and respond with token
    access_token = create_access_token(identity=username)
   
    # default set cookie
    response = jsonify(access_token=access_token)
    # set_access_cookies(response, access_token) # make the set from front end

    # my custome set
    # response = make_response(redirect(url_for("index")))
    response.set_cookie('access_token_cookie', access_token)
    return response
    
@auth_bp.route('/login', methods=['POST'])
def login():
    # getting criedentials from BODY
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # getting criedentials from HEADER
    # auth = request.authorization
    # username = auth.username
    # password = auth.password

    # check on existing
    user = users.find_one({'username': username})
    if user is None:
        return "No such user."
    if password != user['password']:
        return "Wrong password."
    
    # create token
    access_token = create_access_token(identity=username)

    # default set cookie
    response = jsonify(access_token=access_token)
    # set_access_cookies(response, access_token) # make the set from front end

    # my custome set
    # response = make_response(redirect(url_for("index")))
    response.set_cookie('access_token_cookie', access_token)
    return response


@auth_bp.route('/logout')
@jwt_required
def logout():
    response = jsonify(message='Logged Out!')
    unset_jwt_cookies(response)
    return response, 200

@app.route('/')
@jwt_required
def index():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)