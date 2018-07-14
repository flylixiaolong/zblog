from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user
from blog.models import Admin
from blog import db

admin_api = Blueprint('admin_api', __name__, url_prefix='/api/admin', template_folder='templates')

@admin_api.route('/token', methods=['GET', 'POST'])
def auth_token():
    if g.current_user.is_anonymous:
        return unauthorized('Invalid credentials')
    if not g.token_used:
        return jsonify({'token': g.current_user.generate_auth_token(), 'expiration': 3600})
    else:
        return jsonify({'auth': 'success'})

@admin_api.errorhandler(ResourceError)
def handle_resource_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@admin_api.errorhandler(404)
def handle_url_not_found(error):
    response = jsonify({"error": "Resource Not Found"})
    return response