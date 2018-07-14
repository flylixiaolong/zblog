from flask import jsonify

class ResourceError(Exception):
    status_code = 404
    message = 'Resource Not Found'

    def __init__(self, message, status_code=None, **kwargs):
        super().__init__()
        if message:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.rv = kwargs

    def to_dict(self):
        rv = self.rv
        rv['message'] = self.message
        return rv

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

