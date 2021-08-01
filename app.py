from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import redirect

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        #TODO push new task to the db
        return redirect('/')
    else:
        #TODO grab all tasks from the db
        tasks = [
            {
                'content': 'hello',
                'due': 'today'
            }
        ]

        return render_template('index.html', context=tasks)

@app.route('/del/<int:id>')
def delete(id):

    #TODO grab the task from the db with the id
    tasks = [
            {
                'content': 'hello',
                'due': 'today'
            },

            {
                'content': 'hi',
                'due': 'tomorrow'
            }
        ]
    tasks.pop(id)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)