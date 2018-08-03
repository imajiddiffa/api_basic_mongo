import logging.config
import os

from flask import Flask

from flask_jwt import JWT

from model.base import db


# _jwt = JWT(
#     authentication_handler=User.authenticate, identity_handler=User.identity)

import routes


def create_app(configuration):
    app = Flask(__name__.split(',')[0])
    app.config.from_object(configuration)

    # Register route blueprint
    app.register_blueprint(routes.berita.bp)
    #app.register_blueprint(routes.user)

    # # setting jwt
    #_jwt.init_app(app)

    # # pymongo
    db.init_app(app)

    return app
