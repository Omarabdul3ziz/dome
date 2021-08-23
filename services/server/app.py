from flask import Flask, jsonify, request
from pymongo import MongoClient 
from time import time
from bson.objectid import ObjectId
import os
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)

CORS(app)

# ----> Creating/Connecting Db
MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
DATABASE_URL = f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongo:27017'

# -----> working locally, uncomment this.
DATABASE_URL = 'mongodb://localhost:27017'

client = MongoClient(DATABASE_URL)
database = client['dome_database']
col = database['tasks']

app.config["MONGO_URI"] = DATABASE_URL

api = Api(app)

# -----> restful 
class Tasks(Resource):
    def get(self):
        cursor = col.find({})
        tasks = list_queries(cursor)
        return jsonify({'Tasks': tasks})

    def post(self):
        new_task = {'title' : request.json['title'], 'status': False, 'due': time()} 
        col.insert_one(new_task)
        return 201

class Task(Resource):
    def get(self, index):
        id = get_id(index)
        cursor = col.find({"_id": ObjectId(id)})
        task = list_queries(cursor)
        return jsonify({'Tasks': task})

    def put(self, index):
        id = get_id(index)
        col.update_one({"_id": ObjectId(id)}, {"$set": {'title': request.json['title']}}, upsert=True)
        return 201
    
    def delete(self, index):
        id = get_id(index)
        col.delete_one({"_id": ObjectId(id)})
        return 204

class Status(Resource):
    def put(self, index):
        id = get_id(index)
        col.update_one({'_id': ObjectId(id)}, {"$set": {'status': request.json['status']}}, upsert=True)
        return 201

api.add_resource(Tasks, '/tasks')
api.add_resource(Task, '/tasks/<int:index>')
api.add_resource(Status, '/tasks/<int:index>/check')

# ----> CRUD API
# @app.route('/tasks', methods=["GET"])
# def get():
#     cursor = col.find({})
#     tasks = list_queries(cursor)
#     return jsonify({'Tasks': tasks})

# @app.route('/tasks', methods=["POST"])
# def post():
#     new_task = {'title' : request.json['title'], 'status': False, 'due': time()} 
#     col.insert_one(new_task)
#     return 'OK'

# @app.route('/tasks/<int:index>', methods=["DELETE"])
# def delete(index):
#     id = get_id(index)
#     col.delete_one({"_id": ObjectId(id)})
#     return 'OK'

# @app.route('/tasks/<int:index>', methods=["PUT"])
# def update(index):
#     id = get_id(index)
#     col.update_one({"_id": ObjectId(id)}, {"$set": {'title': request.json['title']}}, upsert=True)
#     return 'OK'

# Which is the right one? PUT method becouse we update the resources 
# Or GET becouse i just need to reverse and the body will be empty
# @app.route('/tasks/<int:index>/check', methods=['PUT'])
# def check(index):
#     id = get_id(index)
#     col.update_one({'_id': ObjectId(id)}, {"$set": {'status': request.json['status']}}, upsert=True)
#     return 'OK'



# ----> Helper functions
def get_id(index):
    tasks = col.find({})
    task = tasks[index]
    id = task["_id"]
    return id

def list_queries(cursor):
    tasks = []
    for query in cursor:
        tasks.append({'title': query['title'], 'status': query['status'], 'due': query['due']})
    return tasks

# ----> WSGI
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) # host and port in flask container