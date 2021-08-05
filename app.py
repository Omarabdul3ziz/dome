from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, request, redirect, jsonify
from main import app, clc
from bson.json_util import dumps

# import os

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        #TODO push new task to the db
        clc.insert_one({'name': content})
        return redirect('/')
    else:
        #TODO grab all tasks from the db
        tasks = list(clc.find())

        return render_template('index.html', context=tasks)

@app.route('/delete/<id>')
def delete(id):
    clc.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('home'))

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        content = request.form['content']
        id = ObjectId(id)
        clc.update_one({"_id": id}, { '$set' : { "name": content}})
        return redirect(url_for('home'))

    else:
        #TODO grab all tasks from the db
        id = ObjectId(id)
        task = clc.find_one({"_id": id})
        return render_template('update.html', context=task)

# ----> RESTful CRUD API flask app

@app.route('/tasks')
def get_tasks():
    cursor = clc.find({})
    tasks = json_it(cursor)
    return {"Tasks": tasks}

@app.route('/tasks/<id>')
def get_task(id):
    cursor = clc.find({'_id': ObjectId(id)})
    task = json_it(cursor)
    return {"content": task}

@app.route('/add', methods=['POST'])
def add_tasks():
    clc.insert_one({'content': request.json['content'], 'done': False})
    return {"status": "Success"}

@app.route('/delete/<int:index>', methods=['DELETE'])
def del_task(index):
    tasks = clc.find({})
    task = tasks[index]
    id = task["_id"]
    clc.delete_one({"_id": ObjectId(id)})
    return {"status": "Success"}

@app.route('/update/<id>', methods=['PUT'])
def update_task(id):
    clc.update_one({"_id": ObjectId(id)}, {"$set": {'content': request.json['content']}}, upsert=True)
    return {"status": "Success"}


def json_it(cursor):
    content = []
    for query in cursor:
        content.append({'content': query['content'], 'done': query['done']})
    return content


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')