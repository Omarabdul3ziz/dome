from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

connection_url = "mongodb://localhost:27017"

app.config["MONGO_URI"] = connection_url

cluster = MongoClient(connection_url)
db = cluster["mydb"]
clc = db["todos"]
