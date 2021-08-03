from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, request, redirect
from main import app, clc
import os

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




if __name__ == "__main__":
<<<<<<< HEAD:app/app.py
    # app.run(debug=True, host='0.0.0.0', port=8080)
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
=======
    app.run(debug=True)
>>>>>>> parent of 26a56dd... failed dockerization:app.py
