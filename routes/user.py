import json

from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt import jwt_required

from controller import UserController
from exceptions import BadRequest

userController = UserController()

bp = Blueprint(__name__, "user")

@bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    is_admin = request.args.get("is_admin")

    if not is_admin:
        raise BadRequest("is_admin is required", 200, 1)

    result = userController.get_user(is_admin)

    response = {"error": 0, "message": "success", "data": result}

    return jsonify(response)

@bp.route("/user", methods=["POST"])
@jwt_required()
def create_user():
    user_object = request.form.get("user_object")

    try:
        user_object_json = json.loads(user_object)
    except:
        raise BadRequest("user_object is missing or error format", 200, 1)

    try:
        email = user_object_json['email']
        username = user_object_json['username']
        password = user_object_json['password']
        first_name = user_object_json['first_name']
        last_name = user_object_json['last_name']
    except:
        raise BadRequest("email, username, password, first_name or last_name is missing",
                         200, 1)

    params = {
        "email": email,
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }

    result = userController.create_user(**params)

    response = {"message": "success", "error": 0, "data": result}

    return jsonify(response)

@bp.route("/user/<username>", methods=["GET"])
@jwt_required()
def get_single_user(username):

    result = userController.get_user_data(username)

    response = {"error": 0, "message": "success", "data": result}

    return jsonify(response)

@bp.route("/user/<_id>", methods=["PUT"])
@jwt_required()
def update_single_user(_id):
    user_object = request.form.get("user_object")

    try:
        user_object_json = json.loads(user_object)
    except:
        raise BadRequest("user_object is missing or error format", 200, 1)

    result = userController.update_user(_id, user_object_json)

    response = {"error": 0, "message": "success", "data": result}

    return jsonify(response)

@bp.route("/user/<_id>", methods=["DELETE"])
@jwt_required()
def delete_single_user(_id):
    userController.delete_user(_id)

    response = {"error": 0, "message": "success", "data": {}}

    return jsonify(response)