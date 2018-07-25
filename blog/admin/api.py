from flask import Blueprint, jsonify
from flask import g, request, json
from flask_login import login_user
from flask_restful import marshal, fields
from .auth import multi_auth
from .fields import catalog_fields
from .fields import tag_fields
from .fields import post_fields
from .service import create_catalog, query_catalogs, query_catalog_by_id
from .service import create_tag, query_tags, query_tags_by_ids, query_tag_by_id
from .service import create_post, query_posts, query_post_by_id, query_post_by_title
from .parser import parser_catalog, parser_account
from .parser import parser_tag, parser_post
from ..models import Admin
from ..errors import unauthorized, not_found, bad_request
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
def new_catalog():
    args = parser_catalog.parse_args()
    args['created_id'] = g.current_user.id
    created, catalog = create_catalog(**args)
    if(created):
        return jsonify(marshal(catalog, catalog_fields))
    return jsonify({'message': {'catalog': '分类已经存在'}, 'error': 'already existed'})


@admin_api.route('/catalog', methods=["GET"])
def list_catalogs():
    catalogs = query_catalogs()
    return jsonify(marshal(catalogs, catalog_fields))


@admin_api.route('/catalog/<int:id>', methods=["GET"])
def get_catalog(id):
    catalog = query_catalog_by_id(id)
    if(not catalog):
        return not_found('资源不存在')
    return jsonify(marshal(catalog, catalog_fields))


@admin_api.route('/tag', methods=["POST"])
def new_tag():
    args = parser_tag.parse_args()
    args['created_id'] = g.current_user.id
    created, tag = create_tag(**args)
    if(created):
        return jsonify(marshal(tag, tag_fields))
    return jsonify({'message': {'tag': '分类已经存在'}, 'error': 'already existed'})


@admin_api.route('/tag', methods=["GET"])
def list_tags():
    tags = query_tags()
    return jsonify(marshal(tags, tag_fields))


@admin_api.route('/tag/<int:id>', methods=["GET"])
def get_tag(id):
    tag = query_tag_by_id(id)
    if(not tag):
        return not_found('资源不存在')
    return jsonify(marshal(tag, tag_fields))


@admin_api.route('/post', methods=["POST"])
def new_post():
    message = {}
    args = parser_post.parse_args()
    db_catalog = query_catalog_by_id(args.catalog)
    db_tags = query_tags_by_ids(args.tags)
    if not db_catalog:
        message['catalog'] = '`{0}`查询分类失败'.format(args.catalog)
    if len(db_tags) != len(args.tags):
        message['tags'] = '`{0}`查询标签失败'.format(args.tags)
    db_post = query_post_by_title(args.title)
    if db_post:
        message['title'] = '标题已存在'
    if message:
        return bad_request(message)
    args['created_id'] = g.current_user.id
    args['catalog'] = db_catalog
    args['tags'] = db_tags
    created, post = create_post(**args)
    if(created):
        return jsonify(marshal(post, post_fields))
    return jsonify({'message': {'post': '分类已经存在'}, 'error': 'already existed'})


@admin_api.route('/post', methods=["GET"])
def list_posts():
    posts = query_posts()
    return jsonify(marshal(posts, post_fields))


@admin_api.route('/post/<int:id>', methods=["GET"])
def get_post(id):
    post = query_post_by_id(id)
    if(not post):
        return not_found('资源不存在')
    return jsonify(marshal(post, post_fields))