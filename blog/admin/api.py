from flask import Blueprint, jsonify
from flask import g, request
from flask_login import login_user
from .auth import unauthorized, multi_auth
from .parser import parser_catalog, parser_account
from ..models import Admin, Catalog
from .. import db

admin_api = Blueprint('admin_api', __name__, url_prefix='/api/admin', template_folder='templates')

# when you use this all request will be auth
@admin_api.before_request
@multi_auth.login_required
def before_request():
    if request.method != 'OPTIONS' and g.current_user.is_anonymous and request.path != '/api/admin/token':
        return unauthorized('Unauthorized user')


@admin_api.route('/token', methods=['GET', 'POST'])
def auth_token():
    parser_account.parse_args()
    if g.current_user.is_anonymous:
        return unauthorized('Invalid credentials')
    if not g.token_used:
        return jsonify({'token': g.current_user.generate_auth_token(), 'expiration': 3600})
    else:
        return jsonify({'auth': 'success'})


@admin_api.route('/catalog', methods=["POST"])
def create_catalog():
    args = parser_catalog.parse_args()
    args['created_id'] = g.current_user.id
    catalog = Catalog(**args)
    db.session.add(catalog)
    db.session.commit()
    return jsonify(args)


@admin_api.route('/catalog', methods=["GET"])
def list_catalog():
    args = parser_catalog.parse_args()
    return args