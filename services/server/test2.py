from flask import Blueprint, request, jsonify, Flask, make_response

from flask_mongoalchemy import MongoAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, jwt_required

import uuid

app = Flask(__name__)

app.config["MONGOALCHEMY_DATABASE"] = 'test_tasksDb'
app.config["MONGOALCHEMY_CONNECTION_STRING"] = 'mongodb://localhost:27017'

app.config["JWT_SECRET_KEY"] = 'secret'
app.config["JWT_TOKEN_LOCATION"] = ['cookies']
app.config["JWT_COOKIE_SECURE"] = True

db = MongoAlchemy(app=app)
jwt = JWTManager(app=app)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

class User(db.Document):
    id = db.StringField()
    name = db.StringField()
    password = db.StringField()

    def authenticate(username, password):
        user = User.query.filter(User.name==username).first()
        if user.password == password:
            return user

@auth_bp.route('/register', methods=('POST',))
def register():
  data = request.get_json()
  password = data['password']
  username = data['username']

  user = User.query.filter(User.name==username).first()
  if user is None:
    new_user = User(id=str(uuid.uuid4()), name=username, password=password)
    new_user.save()

    token_identity = {"username": username}
    access_token = create_access_token(identity= token_identity)
    refresh_token = create_refresh_token(identity = token_identity) 

    set_access_cookies({"login": True}, access_token)
    set_refresh_cookies({"login": True}, refresh_token)

    response = make_response()
    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)

    return response

    # return jsonify(message=access_token)
  else:
    return jsonify(message="Unable to create user."), 400

@auth_bp.route('/login', methods=('POST',))
def login():
  data = request.get_json()
  username = data['username']
  password = data['password']

  user = User.authenticate(username, password)
  if user:

    token_identity = {"username": username}
    access_token = create_access_token(identity= token_identity)
    refresh_token = create_refresh_token(identity = token_identity) 

    set_access_cookies({"login": True}, access_token)
    set_refresh_cookies({"login": True}, refresh_token)

    response = make_response()
    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)

    return response

    # return jsonify(message=access_token)

  else:
    return jsonify(message="Unauthorized"), 401

@auth_bp.route('/logout', methods=('POST',))
@jwt_required()
def logout():
  access_token = request.cookies.get('access_token')
  request.cookies.clear()
  response = jsonify()
  unset_jwt_cookies(response)
  return access_token


@app.route('/')
def home():
    admin = False
    if admin:
        return {'msg': "Hey admin"}
    else:
        return {'msg': "Hey Guest"}

@app.route('/profile')
@jwt_required()
def profile():
    return {'msg': "Hey User"}

@app.route('/un_protected')
def un_protected():
    return {'msg': "Hey Guest"}

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)