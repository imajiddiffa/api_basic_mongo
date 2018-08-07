from flask import current_app, request

from functools import wraps
from flask_jwt import current_identity

from exceptions import BadRequest


def _validate_app_secret_key():

    secret_key = request.headers.get('X-Api-Key', None)

    if not secret_key == current_app.config['APP_SECRET_KEY']:
        raise BadRequest("Forbidden Access", 403, 1)


def secret_key_required():

    def wrapper(func):

        @wraps(func)
        def decorator(*args, **kwargs):
            _validate_app_secret_key()
            return func(*args, **kwargs)

        return decorator

    return wrapper
