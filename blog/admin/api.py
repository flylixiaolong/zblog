from flask import Blueprint, jsonify
from flask import g, request, json
from flask_login import login_user
from flask_restful import marshal, fields
from .auth import multi_auth
from .fields import catalog_fields, catalogs_fields
from .service import create_catalog, query_catalogs
from .parser import parser_catalog, parser_account
from ..models import Admin, Catalog
from ..errors import unauthorized
from .. import db

admin_api = Blueprint('admin_api', __name__, url_prefix='/api/admin', template_folder='templates')


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
        return jsonify(marshal(catalog, catalog_fields))
    return jsonify({'message': {'catalog': '分类已经存在'}, 'error': 'already existed'})


@admin_api.route('/catalog', methods=["GET"])
def list_catalog():
    catalogs = query_catalogs()
    return jsonify(marshal(catalogs, catalog_fields))