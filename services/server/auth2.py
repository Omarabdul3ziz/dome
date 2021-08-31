from flask import Flask, json, request, jsonify, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from functools import wraps

from flask_dance.contrib.github import make_github_blueprint, github
import os
from flask_login import logout_user, LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./task.db'

db = SQLAlchemy()
db.init_app(app) # db.create_all(app=app)

GITHUB_ID = os.getenv("GITHUB_ID")
GITHUB_SECRET = os.getenv("GITHUB_SECRET")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # to make oath accept not https requests

GITHUB_ID = 'f999c153151ddfb524ce'
GITHUB_SECRET = 'a2a5e3f47e20c2fd0afc3729ce732fe26dba419b'

github_blueprint = make_github_blueprint(client_id=GITHUB_ID, client_secret=GITHUB_SECRET )

app.register_blueprint(github_blueprint, url_prefix='/github_login')

login_manager= LoginManager(app)

# -------- models -------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    token = db.Column(db.String(255))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

def tocken_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify(message='Token is missing!'), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify(message='Token is invalid!'), 401

        if current_user.token != token:
            return jsonify(message='Tokens does not match!, login'), 401

        return func(current_user, *args, **kwargs)
    return wrapper

# -------- auth -------- #

@app.route('/login')
def login():

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if True: # check_password_hash(user.password, auth.password) 
        # proplem in matching
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        user.token = token.decode('UTF-8')
        db.session.commit()
        return jsonify(token=token.decode('UTF-8'))

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')
    if account_info.ok:
        username = account_info.json()['login']

    user = User.query.filter_by(name=username).first()

    if not user:
        return jsonify(message="No such user in Database!")

    if True: # check_password_hash(user.password, auth.password) 
        # proplem in matching
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        user.token = token.decode('UTF-8')
        db.session.commit()
        return jsonify(token=token.decode('UTF-8'))

    return jsonify(message='Request failed')

@app.route('/logout')
@tocken_required
def logout(current_user):
    current_user.token = ''
    db.session.commit()

    return jsonify(message="You are logged out!")

@app.route('/')
def index():
    return '<h1>Homa Page</h1>'

# -------- user api -------- #

@app.route('/user', methods=['GET'])
# @tocken_required
def get_all_users():

    # if not current_user.admin:
    #     return jsonify(message="Do not have privilege")

    users = User.query.all()
    output = []  # to convert from alchemy queries to iterable 
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['token'] = user.token
        output.append(user_data)

    return jsonify(users=output)

@app.route('/user', methods=['POST'])
# @tocken_required
def create_user():

    # if not current_user.admin:
    #     return jsonify(message="Do not have privilege")

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False, token='')
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="New user created!")

@app.route('/user/<public_id>', methods=['GET'])
@tocken_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify(message="Do not have privilege")

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify(message="No user found!")

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['token'] = user.token

    return jsonify(user=user_data)

@app.route('/user/<public_id>', methods=['PUT'])
@tocken_required
def edit_user(current_user, public_id):

    if not current_user.admin:
        return jsonify(message="Do not have privilege")

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify(message="No user found!")

    data = request.get_json()
    user.name = data['name']
    user.password = data['password']
    user.admin = data['admin']
    db.session.commit()

    return jsonify(message="User edited!")

@app.route('/user/<public_id>', methods=['DELETE'])
@tocken_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify(message="Do not have privilege")

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify(message="No user found!")

    db.session.delete(user)
    db.session.commit()

    return jsonify(message="User deleted!")

# -------- todo api -------- #

@app.route('/task', methods=["GET"])
@tocken_required
def get_all_tasks(current_user):

    tasks = Todo.query.filter_by(user_id=current_user.id).all()

    output = []

    for task in tasks:
        data = {}
        data['id'] = task.id
        data['text'] = task.text
        data['complete'] = task.complete
        # data['user_id'] = task.user_id
        output.append(data)

    return jsonify(tasks=output)

@app.route('/task', methods=["POST"])
@tocken_required
def create_task(current_user):
    data = request.get_json()

    new_task = Todo(text=data['text'], complete=False, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(message='Task created!')

@app.route('/task/<task_id>', methods=["GET"])
@tocken_required
def get_one_task(current_user, task_id):
    task = Todo.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify(message="No task found!")

    data = {}
    data['id'] = task.id
    data['text'] = task.text
    data['complete'] = task.complete
    # data['user_id'] = task.user_id

    return jsonify(task=data)

@app.route('/task/<task_id>', methods=["Put"])
@tocken_required
def edit_task(current_user, task_id):
    task = Todo.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify(message="No task found!")
    
    data = request.get_json()

    task.text = data['text']
    task.complete = data['complete']

    db.session.commit()

    return jsonify(message="Task edited!")

@app.route('/task/<task_id>', methods=["DELETE"])
@tocken_required
def delete_task(current_user, task_id):
    task = Todo.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify(message="No task found!")

    db.session.delete(task)
    db.session.commit()

    return jsonify(message="Task deleted!")

@app.route('/task/<task_id>/check', methods=["Put"])
@tocken_required
def check_task(current_user, task_id):
    task = Todo.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify(message="No task found!")
    
    data = request.get_json()

    task.complete = not task.complete

    db.session.commit()

    return jsonify(message="Task checked!")

if __name__ == '__main__':
    app.run(debug=True)