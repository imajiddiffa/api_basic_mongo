import time
import string
import random
from datetime import datetime, timedelta
from dateutil import tz
from exceptions import BadRequest
from bson.objectid import ObjectId
from flask import current_app
from model import db

from passlib.hash import md5_crypt as pwd_context

class UserController(object):
    def authenticate(self, username: 'str', password: 'str') -> 'User':
        user = list(db.db.user.find({ "$or" : [{"username":username}, {"email":username}]}))
        #print("USER ", user)

        if len(user) == 0:
            return None

        user = user[0]
        user["id"] = str(user["_id"])

        if pwd_context.verify(password, user["password"]):
            return user

    def identity(self, payload: 'dict') -> 'User':
        _id = payload['identity']
        user = list(db.db.user.find({"_id": ObjectId(_id)}))
        if len(user) == 0:
            raise KeyError("user not found")

        user = user[0]

        return user

    def jwt_payload_handler(self, identity):
        iat = datetime.utcnow()
        exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
        identity = identity['id']
        return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}
    
    def get_user_data(self, username: str):
        user = list(db.db.user.find({ "$or" : [{"username":username}, {"email":username}]}))

        if len(user) == 0:
            raise BadRequest(
                "This account is not exists, please contact our customer services",
                200, 1)
        else:
            user = user[0]

        if user["is_deleted"] is True:
            raise BadRequest(
                "Your account is deleted, please contact our customer services.",
                200, 2)

        user['_id'] = str(user['_id'])

        return user

    def get_user(self, is_admin):
        try:
            result = list(db.db.user.find({
                "is_admin": is_admin,
            }))
        except:
            result = []
        
        for each_result in result:
            each_result['_id'] = str(each_result['_id'])

        return result

    def create_user(self, **kwargs):
        email = kwargs.get("email")
        username = kwargs.get("username")
        password = kwargs.get("password")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")

        current_date = str(datetime.now())

        result_object = {
            "email": email,
            "username": username,
            "password": pwd_context.encrypt(password),
            "first_name": first_name,
            "last_name": last_name,
            "timezone" : 'Asia/Jakarta',
            "join_date" : str(current_date),
            "expired_date" : str(current_date),
            "confirmation_code" : self.id_generator(),  # generate random code
            "is_active" : True,
            "is_deleted" : False,
            "is_admin" : False,
            "user_type" : "register",
            "picture" : "-"
        }

        result = db.db.user.insert_one(result_object)

        result_object.update({"_id": str(result.inserted_id)})

        return result_object

    def update_user(self, _id, user_object):
        user_type = ""

        try:
            update_result = db.db.user.find_and_modify(
                            query={
                                '_id': ObjectId(_id),
                                "is_deleted": False
                            },
                            update={'$set': user_object},
                            upsert=False,
                            full_response=True)
            try:
                user_type = update_result['value']['user_type']
            except:
                pass
        except:
            raise BadRequest("Something happen when updated data", 200, 1)

        if user_type:
            result = list(
                        db.db.user.find({
                            "is_deleted": False,
                            "type": user_type,
                        }))
        else:
            raise BadRequest("Data already same as updated object", 200, 1)

        for each_result in result:
            each_result['_id'] = str(each_result['_id'])

        return result

    def delete_user(self, _id):
        try:
            # mongo.db.blog.delete_one({'_id': ObjectId(blog_id), 'user_id': user_id})
            db.db.user.find_and_modify(
                query={
                    '_id': ObjectId(_id),
                    "is_deleted": False
                },
                update={'$set': {
                    "is_deleted": True,
                    "is_active": False 
                }},
                upsert=False,
                full_response=True)
        except:
            raise BadRequest("Something happen when updated data", 200, 1)

    def id_generator(self):
        # generate random code
        size = 12
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        code = ''.join(random.choice(chars) for _ in range(size))
        return code