from flask import Flask, jsonify, request
from pymongo import MongoClient 
from time import time
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://mongo:27017' # the hostname and the port inside mongo docker

# ----> Creating/Connecting Db
client = MongoClient('mongodb://mongo:27017')
database = client['dome_database']
col = database['tasks']

# ----> CRUD API
@app.route('/tasks', methods=["GET"])
def get():
    cursor = col.find({})
    tasks = list_queries(cursor)
    return jsonify({'Tasks': tasks})

@app.route('/tasks', methods=["POST"])
def post():
    new_task = {'title' : request.json['title'], 'status': False, 'due': time()} 
    col.insert_one(new_task)
    return 'OK'

@app.route('/tasks/<int:index>', methods=["DELETE"])
def delete(index):
    id = get_id(index)
    col.delete_one({"_id": ObjectId(id)})
    return 'OK'

@app.route('/tasks/<int:index>', methods=["PUT"])
def update(index):
    id = get_id(index)
    col.update_one({"_id": ObjectId(id)}, {"$set": {'title': request.json['title']}}, upsert=True)
    return 'OK'

# Which is the right one? PUT method becouse we update the resources 
# Or GET becouse i just need to reverse and the body will be empty
@app.route('/tasks/<int:index>/check', methods=['GET'])
def check(index):
    id = get_id(index)
    col.update_one({'_id': ObjectId(id)}, {"$set": {'status': request.json['status']}}, upsert=True)
    return 'OK'



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
    app.run(debug=True, host='0.0.0.0', port=11) # host and port in flask container