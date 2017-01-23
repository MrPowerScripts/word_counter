import jwt
import json
from functools import wraps
from flask import g, request, redirect, url_for, jsonify
from settings import Config
import logging


def api_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        auth = request.headers.get('Authorization')

        if not auth:
            return jsonify({"error": "unauthorized header"}), 403

        token = str.split(
            auth.encode("utf-8"), " ")[1]

        try:
            g.user = jwt.decode(token,
                                Config.SECRET_KEY,
                                algorithms=['HS256'])

            return f(*args, **kwargs)
        except jwt.DecodeError as e:
            logging.error(e)
            return jsonify({"error": "expired token"}), 302

    return decorated_function


def provider_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        auth = request.headers.get('Authorization')

        if not auth:
            return jsonify({"error": "unauthorized header"}), 403

        token = str.split(
            auth.encode("utf-8"), " ")[1]

        try:
            g.user = jwt.decode(token,
                                Config.SECRET_KEY,
                                algorithms=['HS256'])

            if g.user["provider"]:
                return jsonify({"error": "unauthorized account type"}), 403

            return f(*args, **kwargs)
        except jwt.DecodeError as e:
            logging.error(e)
            return jsonify({"error": "expired token"}), 302

    return decorated_function


def api_token_optional(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        auth = request.headers.get('Authorization')

        if not auth:

            # If authorziation header is not provided this is an anonymous user
            # Setting the global user to True so we can check for anonymous
            # on queries
            g.user = True
            return f(*args, **kwargs)

        token = str.split(auth.encode("utf-8"), " ")[1]

        try:
            g.user = jwt.decode(token,
                                Config.SECRET_KEY,
                                algorithms=['HS256'])

            return f(*args, **kwargs)
        except jwt.DecodeError as e:
            jsonify({"error": "expired token"}), 302
            logging.error(e)

            # Setting the global user to True so we can check for anonymous
            # on queries
            g.user = True
            return f(*args, **kwargs)

    return decorated_function
