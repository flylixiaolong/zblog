from flask import jsonify

def bad_request(error):
    response = jsonify({'message': 'bad request', 'error': error})
    response.status_code = 400
    return response


def unauthorized(error):
    response = jsonify({'message': 'unauthorized', 'error': error})
    response.status_code = 401
    return response


def forbidden(error):
    response = jsonify({'message': 'forbidden', 'error': error})
    response.status_code = 403
    return response

def not_found(error):
    response = jsonify({'message': 'not found', 'error': error})
    response.status_code = 404
    return response