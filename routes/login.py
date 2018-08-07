import json

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app
from exceptions import BadRequest
from werkzeug.local import LocalProxy

from controller import UserController

import traceback

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])
userController = UserController()

bp = Blueprint(__name__, "login")

@bp.route("/login", methods=["POST"])
def auth():
    jwt_access_token = None
    identity = None
    username = request.form.get("username")  # this is user username for login
    password = request.form.get("password")  # this is user password for login

    # validation if username parameter is missing
    if not username:
        raise BadRequest("username is missing", 200, 1)
    if not password:
        raise BadRequest("password is missing", 200, 1)
    # Get user data
    username = username.lower()
    user = userController.get_user_data(username)

    # validation if account still not active
    if user["is_active"] is False:
        raise BadRequest(
            "Your Account is inactive, please contact our customer services.",
            200, 3)
    
    # Set jwt access token
    try:
        identity = _jwt.authentication_callback(username, password)
        #print("IDENTITIYNYA: ", identity)
    except Exception:
        traceback.print_exc()

    if identity:
        try:
            _jwt.jwt_payload_callback = userController.jwt_payload_handler
            jwt_access_token = _jwt.jwt_encode_callback(identity)
            jwt_access_token = jwt_access_token.decode("utf8")
        except Exception:
            traceback.print_exc()

        try:
            default_preset_id = user["default_preset_id"]
        except:
            default_preset_id = None

        # success response
        response = {
            "error": 0,
            "message": 'success',
            "data": {
                "username": user["username"],
                "email": user["email"],
                "picture": user["picture"],
                "is_admin": user["is_admin"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "default_preset_id": default_preset_id,
                "jwt_access_token": jwt_access_token,
                "ad_accounts": "-",
                "timezone": user["timezone"],
            }
        }
        return jsonify(response)

    # failed response
    else:
        raise BadRequest("Wrong username or password", 200, 1)
        #raise JWTError('Bad Request', 'Invalid credentials')

    