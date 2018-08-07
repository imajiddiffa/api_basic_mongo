import logging.config
import os

from flask import Flask

from flask_jwt import JWT

from model.base import db
from controller import UserController

userController = UserController()

_jwt = JWT(
    authentication_handler=userController.authenticate, identity_handler=userController.identity)

import routes


def create_app(configuration):
    app = Flask(__name__.split(',')[0])
    app.config.from_object(configuration)

    # Register route blueprint
    app.register_blueprint(routes.berita.bp)
    app.register_blueprint(routes.login.bp)
    app.register_blueprint(routes.user.bp)

    # setting jwt
    _jwt.init_app(app)

    # pymongo
    db.init_app(app)

    return app
