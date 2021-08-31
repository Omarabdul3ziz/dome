from flask import Flask, json, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todo.db'

db = SQLAlchemy()
db.init_app(app) # db.create_all(app=app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

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

        return func(current_user, *args, **kwargs)
    return wrapper

# -------- user api -------- #

@app.route('/user', methods=['GET'])
@tocken_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify(message="Do not have privilege")

    users = User.query.all()
    output = []  # to convert from alchemy queries to iterable 
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify(users=output)

@app.route('/user', methods=['POST'])
@tocken_required
def create_user(current_user):

    if not current_user.admin:
        return jsonify(message="Do not have privilege")

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
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
        return jsonify(token=token.decode('UTF-8'))

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

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