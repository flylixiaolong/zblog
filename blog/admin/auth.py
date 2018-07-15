from flask import g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from ..models import Admin, AnonymousUser
from ..errors import unauthorized


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='JWT')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(email, password):
    if request.method == 'POST':
        json_dict = request.get_json(cache=True) or request.form
        email = json_dict['email']
        password = json_dict['password']
    if email == '':
        g.current_user = AnonymousUser()
        return True
    user = Admin.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@token_auth.verify_token
def verify_token(token):
    g.current_user = Admin.verify_auth_token(token)
    if g.current_user is None:
        return False
    g.token_used = True
    return True


@basic_auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')
