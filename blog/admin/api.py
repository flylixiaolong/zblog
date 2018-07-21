from flask import Blueprint, jsonify
from flask import g, request
from werkzeug.exceptions import BadRequest, NotFound
from flask_login import login_user
from .auth import multi_auth
from .service import create_catalog
from .parser import parser_catalog, parser_account
from ..models import Admin, Catalog
from ..errors import bad_request, unauthorized, not_found
from .. import db

admin_api = Blueprint('admin_api', __name__, url_prefix='/api/admin', template_folder='templates')

# when you use this all request will be auth
@admin_api.before_request
@multi_auth.login_required
def before_request():
    if request.method != 'OPTIONS' and g.current_user.is_anonymous and request.path != '/api/admin/token':
        return unauthorized('Unauthorized user')

# 400错误处理
@admin_api.errorhandler(BadRequest)
def handle_bad_request(e):
    message = e.data and e.data['message'] or e.message
    return bad_request(message)

# 404错误处理
@admin_api.errorhandler(NotFound)
def handle_not_found(e):
    message = e.data and e.data['message'] or '未找到资源'
    return not_found(message)

# 获取认证token
@admin_api.route('/token', methods=['GET', 'POST'])
def auth_token():
    args = parser_account.parse_args()
    if g.current_user.is_anonymous:
        return unauthorized('Invalid credentials')
    if not g.token_used:
        return jsonify({'token': g.current_user.generate_auth_token(), 'expiration': 3600})
    else:
        return jsonify({'auth': 'success'})


@admin_api.route('/catalog', methods=["POST"])
def create():
    args = parser_catalog.parse_args()
    args['created_id'] = g.current_user.id
    created, catalog = create_catalog(**args)
    if(created):
        return jsonify(catalog)
    return jsonify({'message': {'catalog': '分类已经存在'}, 'error': 'already existed'})


@admin_api.route('/catalog', methods=["GET"])
def list_catalog():
    args = parser_catalog.parse_args()
    return args