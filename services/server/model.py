from flask_login import UserMixin
from flask_mongoalchemy import MongoAlchemy

db = MongoAlchemy()

class User(UserMixin, db.Document):
    id = db.StringField()
    name = db.StringField()
    password = db.StringField()
    admin = db.IntField()

class Task(db.Document):
    id = db.StringField()
    text = db.StringField()
    complete = db.IntField()
    author_id = db.StringField()