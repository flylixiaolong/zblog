from flask import jsonify
from applications.error import ResourceError
from . import admin_api, rest_api


class ValidationError(ValueError):
    pass


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(ResourceError)
def handle_resource_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@api.errorhandler(404)
def handle_url_not_found(error):
    response = jsonify({"error": "Resource Not Found"})
    return response
