from flask import Flask, request, jsonify, make_response, redirect, url_for, Blueprint
from flask_dance.contrib.github import make_github_blueprint, github
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, unset_jwt_cookies, set_access_cookies

import os

from model import users

GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")


auth_blueprint = Blueprint('auth_blueprint', __name__)

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )

#########################################
## =============  Auth   ============= ##
#########################################
@auth_blueprint.route('/github')
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


@auth_blueprint.route('/register', methods=['POST'])
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
    
@auth_blueprint.route('/login', methods=['POST'])
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


@auth_blueprint.route('/logout')
@jwt_required
def logout():
    response = jsonify(message='Logged Out!')
    unset_jwt_cookies(response)
    return response, 200


# @auth_blueprint.route('/')
# @jwt_required
# def home():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
