from flask import jsonify, request, Blueprint
from flask_restful import Resource, Api

import uuid

from auth import login_required, current_user
from model import User, Task

api = Api()

#########################################
## =============  Users  ============= ##
#########################################

class UsersResource(Resource):
    @login_required
    def get(self):
            
        if not current_user.admin:
            return jsonify(message="Do not have privilege")

        users = User.query.all()
        output = [] 
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify(users=output)

    @login_required
    def post(self):
            
        if not current_user.admin:
            return jsonify(message="Do not have privilege")

        data = request.get_json()
        new_user = User(id=str(uuid.uuid4()), name=data['name'], password=data['password'], admin=data['admin'])
        new_user.save()

        return jsonify(message="New user created!")

class UserResource(Resource):
    @login_required
    def get(self, public_id):
            
        if not current_user.admin:
            return jsonify(message="Do not have privilege")

        user = User.query.filter(User.id==public_id).first()

        if not user:
            return jsonify(message="No user found!")

        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        return jsonify(user=user_data)

    @login_required
    def put(self, public_id):
            
        if not current_user.admin:
            return jsonify(message="Do not have privilege")

        user = User.query.filter(User.id==public_id).first()

        if not user:
            return jsonify(message="No user found!")

        data = request.get_json()
        user.name = data['name']
        user.password = data['password']
        user.admin = data['admin']
        user.save()

        return jsonify(message="User edited!")

    @login_required
    def delete(self, public_id):
            
        if not current_user.admin:
            return jsonify(message="Do not have privilege")

        user = User.query.filter(User.id==public_id).first()

        if not user:
            return jsonify(message="No user found!")

        user.remove()

        return jsonify(message="User deleted!")

class TasksResource(Resource):
    @login_required
    def get(self):
            
        tasks = Task.query.filter(Task.author_id == current_user.id).all()
        # tasks = Task.query.all()

        output = []
        for task in tasks:
            data = {}
            data['id'] = task.id
            data['text'] = task.text
            data['complete'] = task.complete
            # data['user'] = current_user.name
            output.append(data)

        return jsonify(tasks=output)

    @login_required
    def post(self):
        
        data = request.get_json()

        new_task = Task(id=str(uuid.uuid4()), text=data['text'], complete=0, author_id=current_user.id)
        new_task.save()

        return jsonify(message='Task created!')

class TaskResource(Resource):
    @login_required
    def get(self, task_id):
        
        task = Task.query.filter(Task.id == task_id, Task.author_id ==current_user.id).first()
        if not task:
            return jsonify(message="No task found!")

        data = {}
        data['id'] = task.id
        data['text'] = task.text
        data['complete'] = task.complete
        data['user'] = current_user.name

        return jsonify(task=data)

    @login_required
    def put(self, task_id):
        
        task = Task.query.filter(Task.id==task_id, Task.author_id==current_user.id).first()
        if not task:
            return jsonify(message="No task found!")
        
        data = request.get_json()

        task.text = data['text']
        task.save()

        return jsonify(message="Task edited!")

    @login_required
    def delete(self, task_id):
        task = Task.query.filter(Task.id==task_id, Task.author_id==current_user.id).first()
        if not task:
            return jsonify(message="No task found!")

        task.remove()

        return jsonify(message="Task deleted!")

class Status(Resource):
    @login_required
    def put(self, task_id):
        
        task = Task.query.filter(Task.id==task_id, Task.author_id==current_user.id).first()
        if not task:
            return jsonify(message="No task found!")
        
        task.complete = not task.complete
        task.save()

        return jsonify(message="Task checked!")

api.add_resource(UsersResource, '/user')
api.add_resource(UserResource, '/user/<public_id>')

api.add_resource(TasksResource, '/task')
api.add_resource(TaskResource, '/task/<task_id>')

api.add_resource(Status, '/task/<task_id>/check')
