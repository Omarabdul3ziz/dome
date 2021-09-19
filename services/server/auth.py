from flask import Flask, request, jsonify, make_response, redirect, url_for, Blueprint, json, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, unset_jwt_cookies, set_access_cookies
from urllib.parse import urlencode
from uuid import uuid4
import requests
import os

from model import users

GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")


auth_blueprint = Blueprint('auth_blueprint', __name__)
tribot_bp = Blueprint('threebot_blueprint', __name__)

github_blueprint = make_github_blueprint(
    client_id=GITHUB_ID, client_secret=GITHUB_SECRET)

#########################################
## ==========  3 bot Auth   ========== ##
#########################################

# APIs URL
PROXY_OAUTH_SERVER_URL = "http://127.0.0.1:9000"
HOST_URL = 'https://login.threefold.me'

# App info
APP_ID = '127.0.0.1:5000'
REDIRECT_ROUTE = "/3bot/callback"


def generate_login_url():

    state = str(uuid4()).replace("-", "")
    session["state"] = state

    response = requests.get(f"{PROXY_OAUTH_SERVER_URL}/pubkey")
    # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    response.raise_for_status()
    data = response.json()
    pubkey = data["publickey"].encode()

    params = {
        "state": state,
        "appid": APP_ID,
        "scope": json.dumps({"user": True, "email": True}),
        "redirecturl": REDIRECT_ROUTE,
        "publickey": pubkey,
    }

    url_params = urlencode(params)
    return f"{HOST_URL}?{url_params}"


@tribot_bp.route("/login")
def tribot_login():
    return redirect(generate_login_url())


@tribot_bp.route("/callback")
def callback():
    state = session["state"]
    signed_attempt_val = request.args.get("signedAttempt")

    data = {
        "signedAttempt": signed_attempt_val,
        "state": state
    }

    response = requests.post(f"{PROXY_OAUTH_SERVER_URL}/verify", data=data)
    response.raise_for_status()

    account_info = response.json()

    username = account_info['username']
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

    response = make_response(redirect("http://127.0.0.1:8080/"))
    response.set_cookie("access_token_cookie", access_token)
    return response

#########################################
## =========  github Auth   ========== ##
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

#########################################
## ==========  basic Auth   ========== ##
#########################################


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
@jwt_required()
def logout():
    response = jsonify(message='Logged Out!')
    unset_jwt_cookies(response)
    return response, 200


# @auth_blueprint.route('/')
# @jwt_required
# def home():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
