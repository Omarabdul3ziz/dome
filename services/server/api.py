from flask import jsonify, request, Blueprint
from flask_restful import Resource, Api

from bson import ObjectId
from auth import jwt_required, get_jwt_identity
from model import users, tasks

api = Api()

#########################################
## =============  Users  ============= ##
#########################################


class TasksResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        current_user = users.find_one({"username": current_user})

        tasks_list = tasks.find({"author": current_user['username']})

        output = []
        for task in tasks_list:
            data = {}
            data['_id'] = str(task['_id'])
            data['text'] = task['text']
            data['complete'] = task['complete']
            output.append(data)

        return jsonify(tasks=output)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        current_user = users.find_one({"username": current_user})

        data = request.get_json()

        new_task = {"text": data['text'], "complete": False, "author": current_user['username']}
        tasks.insert(new_task)

        return jsonify(message='Task created!')


class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):

        current_user = get_jwt_identity()
        current_user = users.find_one({"username": current_user})

        task = tasks.find_one({"author": current_user['username'], "_id": ObjectId(task_id)})

        if not task:
            return jsonify(message="No task found!")

        data = {}
        data['_id'] = str(task['_id'])
        data['text'] = task['text']
        data['complete'] = task['complete']

        return jsonify(task=data)

    @jwt_required()
    def put(self, task_id):

        current_user = get_jwt_identity()
        current_user = users.find_one({"username": current_user})

        task = tasks.find_one({"author": current_user['username'], "_id": ObjectId(task_id)})

        if not task:
            return jsonify(message="No task found!")

        data = request.get_json()
        new_task = {"text": data['text']}
        tasks.update(task, {"$set": new_task})

        return jsonify(message="Task edited!")

    @jwt_required()
    def delete(self, task_id):

        current_user = get_jwt_identity()
        current_user = users.find_one({"username": current_user})

        task = tasks.find_one({"author": current_user['username'], "_id": ObjectId(task_id)})
        if not task:
            return jsonify(message="No task found!")

        tasks.remove(task)

        return jsonify(message="Task deleted!")


class Status(Resource):
    @jwt_required()
    def put(self, task_id):
        current_user = get_jwt_identity()
        current_user = users.find_one({"username": current_user})

        task = tasks.find_one({"author": current_user['username'], "_id": ObjectId(task_id)})

        if not task:
            return jsonify(message="No task found!")

        status = task['complete']
        new_task = {"complete": not status }
        tasks.update(task, {"$set": new_task})

        return jsonify(message="Task checked!")


api.add_resource(TasksResource, '/task')
api.add_resource(TaskResource, '/task/<task_id>')
api.add_resource(Status, '/task/<task_id>/check')


#TODO: implement the user management system
def user_api():
    # class UsersResource(Resource):
    #     @jwt_required
    #     def get(self):
    #         current_user = get_jwt_identity()
    #         current_user = users.find_one({"username": current_user})
    #         if not current_user['admin']:
    #             return jsonify(message="Do not have privilege")

    #         users_list = users.find({})
    #         output = []
    #         for user in users_list:
    #             user_data = {}
    #             user_data['username'] = user['username']
    #             user_data['password'] = user['password']
    #             user_data['admin'] = user['admin']
    #             output.append(user_data)

    #         return jsonify(users_list=output)

    #     @jwt_required
    #     def post(self):
    #         current_user = get_jwt_identity()
    #         current_user = users.find_one({"username": current_user})
    #         if not current_user['admin']:
    #             return jsonify(message="Do not have privilege")

    #         data = request.get_json()
    #         new_user = {"name":data['name'], "password":data['password'], "admin":data['admin']}
    #         users.insert_one(new_user)

    #         return jsonify(message="New user created!")


    # class UserResource(Resource):
    #     @jwt_required
    #     def get(self, public_id):

    #         current_user = get_jwt_identity()
    #         current_user = users.find_one({"username": current_user})
    #         if not current_user['admin']:
    #             return jsonify(message="Do not have privilege")

    #         user = users.find({"username": current_user.username})

    #         if not user:
    #             return jsonify(message="No user found!")

    #         user_data = {}
    #         user_data['id'] = user['id']
    #         user_data['name'] = user['name']
    #         user_data['password'] = user['password']
    #         user_data['admin'] = user['admin']

    #         return jsonify(user=user_data)

    #     @jwt_required
    #     def put(self, public_id):

    #         current_user = get_jwt_identity()
    #         current_user = users.find_one({"username": current_user})
    #         if not current_user['admin']:
    #             return jsonify(message="Do not have privilege")

    #         user = users.find({"username": current_user.username})

    #         if not user:
    #             return jsonify(message="No user found!")

    #         data = request.get_json()
            
    #         users.update_one(user, {"$set": data})

    #         return jsonify(message="User edited!")

    #     @jwt_required
    #     def delete(self, public_id):

    #         current_user = get_jwt_identity()
    #         current_user = users.find_one({"username": current_user})
    #         if not current_user['admin']:
    #             return jsonify(message="Do not have privilege")

    #         user = users.find({"username": current_user.username})

    #         if not user:
    #             return jsonify(message="No user found!")

    #         users.delete_one(user)

    #         return jsonify(message="User deleted!")


    # api.add_resource(UsersResource, '/user')
    # api.add_resource(UserResource, '/user/<public_id>')
    pass