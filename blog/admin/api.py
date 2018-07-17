from flask import Blueprint, jsonify
from flask import g, request
from flask_login import login_user
from .auth import unauthorized, multi_auth
from ..models import Admin
from .. import db

admin_api = Blueprint('admin_api', __name__, url_prefix='/api/admin', template_folder='templates')

@admin_api.route('/token', methods=['GET', 'POST'])
def auth_token():
    if g.current_user.is_anonymous:
        return unauthorized('Invalid credentials')
    if not g.token_used:
        return jsonify({'token': g.current_user.generate_auth_token(), 'expiration': 3600})
    else:
        return jsonify({'auth': 'success'})


# when you use this all request will be auth
@admin_api.before_request
@multi_auth.login_required
def before_request():
    if request.method != 'OPTIONS' and g.current_user.is_anonymous:
        return unauthorized('Unauthorized user')
