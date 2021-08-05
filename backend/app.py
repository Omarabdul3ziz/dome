from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, request, redirect, jsonify
from bson.json_util import dumps

from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app) # This makes the CORS feature cover all routes in the app

connection_url_at_docker = "mongodb://mongo:27017"
connection_url_at_host = "mongodb://localhost"

app.config["MONGO_URI"] = connection_url_at_docker

cluster = MongoClient(connection_url_at_docker)
db = cluster["mydb"]
clc = db["todos"]


# ----> RESTful CRUD API flask app

@app.route('/api/')
def get_tasks():
    cursor = clc.find({})
    tasks = json_it(cursor)
    return {"Tasks": tasks}

@app.route('/api/add', methods=['POST'])
def add_tasks():
    clc.insert_one({'content': request.json['content'], 'done': False})
    return {"status": "Success"}

@app.route('/api/delete/<int:index>', methods=['DELETE'])
def del_task(index):
    id = get_id(index)
    clc.delete_one({"_id": ObjectId(id)})
    return {"status": "Success"}

@app.route('/api/update/<int:index>', methods=['PUT'])
def update_task(index):
    id = get_id(index)
    clc.update_one({"_id": ObjectId(id)}, {"$set": {'content': request.json['content']}}, upsert=True)
    return {"status": "Success"}

@app.route('/api/check/<int:index>', methods=['PUT'])
def check(index):
    id = get_id(index)
    clc.update_one({'_id': ObjectId(id)}, {"$set": {'done': request.json['done']}}, upsert=True)
    return {'status': "Success"}


# ----> Helper functions
def get_id(index):
    tasks = clc.find({})
    task = tasks[index]
    id = task["_id"]
    return id

def json_it(cursor):
    content = []
    for query in cursor:
        content.append({'content': query['content'], 'done': query['done']})
    return content