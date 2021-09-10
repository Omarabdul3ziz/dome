from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, g, jsonify
from pymongo import MongoClient
from functools import wraps
from flask_dance.contrib.github import make_github_blueprint, github
import os


GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['dome2']
users = db['users']
tasks = db['tasks']

app.config['SECRET_KEY'] = 'secret'

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )
app.register_blueprint(github_blueprint, url_prefix="/login")

@app.route('/github_login')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')
    if account_info.ok:
        username = account_info.json()['login']

    user = users.find_one({'username': username})

    if user is None:
        user = {'username': username,
                'password': "",
                'admin': False}

        users.insert(user)
        
    session.clear()
    session['username'] = user['username']
    load_user()
    return redirect(url_for('index'))


@auth_bp.route('/register', methods=['POST'])
def register():
    # if request.method == 'POST':
    auth = request.authorization
    username = auth.username
    password = auth.password

    if not username:
        return 'Username is required.'
    if not password:
        return 'Password is required.'
    
    user = {'username': username,
            'password': password,
            'admin': False}

    users.insert(user)
    return redirect(url_for("auth.login"))
    
    # return render_template("register.html")

@auth_bp.route('/login', methods=['POST'])
def login():
    # if request.method == 'POST':
    auth = request.authorization
    username = auth.username
    password = auth.password

    user = users.find_one({'username': username})
    if user is None:
        return "No such user."
    if password != user['password']:
        return "Wrong password."
    
    session.clear()
    session['username'] = user['username']
    return redirect(url_for('index'))

    # return render_template('login.html')

@auth_bp.before_app_request
def load_user():
    username = session.get('username')
    g.user = users.find_one({'username': username})


def login_required(func):
    @wraps(func)
    def wrapper(**kwargs):
        if g.user is None:
            return jsonify(message="Login required!")
            # return redirect(url_for('auth.login'))
        return func(**kwargs)
    return wrapper


@auth_bp.route('logout')
@login_required
def logout():
    session.clear()
    return jsonify(message='Loged Out!')
    # return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    user = g.user['username']
    tasks = {}
    return jsonify(user=user, tasks=tasks)
    # return render_template('home.html')

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)