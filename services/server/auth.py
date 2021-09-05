from flask import Flask, request, jsonify, make_response, redirect, url_for, Blueprint
from flask_dance.contrib.github import make_github_blueprint, github
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

import os
import uuid

from model import User

GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

login_manager = LoginManager()

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )
login_blueprint = Blueprint('login', __name__)

#########################################
## =============  Auth   ============= ##
#########################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==user_id).first()

@login_blueprint.route('/github')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')
    if account_info.ok:
        username = account_info.json()['login']

    user = User.query.filter(User.name==username).first()

    if not user:
        new_user = User(id=str(uuid.uuid4()), name=username, password="", admin=1)
        new_user.save()

    login_user(user)
    return jsonify(message="You are logged in!")

@login_blueprint.route('/login')
def login():
    auth = request.authorization
    password = auth.password
    username = auth.username
    user = User.query.filter(User.name==username).first()

    if not auth or not username or not password:
        return make_response('Some auth missing!', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if not user:
        return make_response('User not found in database!', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if user.password != password:
        return make_response('Wrong password', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    login_user(user)
    return jsonify(message="You are logged in!")

@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message="You are logged out!")

@login_blueprint.route('/profile')
@login_required
def home():
    return jsonify(message="Welcome "+ current_user.name)


@login_blueprint.route('/') # callback after github login
def index():
    return redirect(url_for('login.github_login'))
