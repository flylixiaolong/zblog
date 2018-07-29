from flask import Blueprint, jsonify
from flask import g, request, json
from flask_login import login_user
from flask_restful import marshal
from .auth import multi_auth
from .fields import catalog_fields, tag_fields
from .fields import post_fields, comment_fields
from .service import create_catalog, query_catalogs, query_catalog_by_id
from .service import create_tag, query_tags, query_tags_by_ids, query_tag_by_id
from .service import create_post, query_posts, query_post_by_id, query_post_by_title
from .service import total_posts, create_comment
from .parser import parser_catalog, parser_account, parser_pagination
from .parser import parser_tag, parser_post, parser_comment
from ..models import Admin
from ..utils import paging
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
    return jsonify({'error': {'catalog': '分类已经存在'}, 'message': 'already existed'})


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
    return jsonify({'error': {'tag': '分类已经存在'}, 'message': 'already existed'})


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
    error = {}
    args = parser_post.parse_args()
    db_catalog = query_catalog_by_id(args.catalog)
    db_tags = query_tags_by_ids(args.tags)
    if not db_catalog:
        error['catalog'] = '`{0}`查询分类失败'.format(args.catalog)
    if len(db_tags) != len(args.tags):
        error['tags'] = '`{0}`查询标签失败'.format(args.tags)
    if error:
        return bad_request(error)
    args['created_id'] = g.current_user.id
    args['catalog'] = db_catalog
    args['tags'] = db_tags
    created, post = create_post(**args)
    if(created):
        return jsonify(marshal(post, post_fields))
    return jsonify({'error': {'title': '标题已存在'}, 'message': 'already existed'})


@admin_api.route('/post', methods=["GET"])
def list_posts():
    page_args = parser_pagination.parse_args()
    posts = query_posts(**page_args)
    total = total_posts()
    page_args['total'] = total
    return jsonify(paging(marshal(posts, post_fields), **page_args))


@admin_api.route('/post/<int:id>', methods=["GET"])
def get_post(id):
    post = query_post_by_id(id)
    if(not post):
        return not_found('资源不存在')
    return jsonify(marshal(post, post_fields))


# 处理评论相关数据
@admin_api.route('/comment', methods=["POST"])
def new_comment():
    args = parser_comment.parse_args()
    error, comment = create_comment(**args)
    if(error):
        return bad_request(error)
    return jsonify(marshal(comment, comment_fields))


@admin_api.route('/comment', methods=["GET"])
def list_comments():
    page_args = parser_pagination.parse_args()
    comments = query_comments(**page_args)
    total = total_comments()
    page_args['total'] = total
    return jsonify(paging(marshal(comments, comment_fields), **page_args))


@admin_api.route('/comment/<int:id>', methods=["GET"])
def get_comment(id):
    comment = query_comment_by_id(id)
    if(not comment):
        return not_found('资源不存在')
    return jsonify(marshal(comment, comment_fields))