from flask import Flask
from pymongo import MongoClient

import os 

app = Flask(__name__)

connection_url = "mongodb://localhost:27017"
# connection_url = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

app.config["MONGO_URI"] = connection_url

cluster = MongoClient(connection_url)
db = cluster["mydb"]
clc = db["todos"]
