from flask_mongoengine import MongoEngine
from flask import Flask
from flask_login import UserMixin, LoginManager

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb://localhost:27017'
}

db = MongoEngine(app)



class User(UserMixin, db.Document):
    meta = {'collection': 'user'}
    username = db.StringField(max_length=30)
    password = db.StringField()
    authenticated = db.BoolenField()

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.find(user_id)
