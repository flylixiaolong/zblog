from flask import request, g, jsonify
from werkzeug import exceptions
from ..errors import unauthorized, bad_request, not_found, forbidden
from .api import admin_api
from .auth import multi_auth

# when you use this all request will be auth
@admin_api.before_request
@multi_auth.login_required
def before_request():
    if request.method != 'OPTIONS' and g.current_user.is_anonymous and request.path != '/api/admin/token':
        return unauthorized('Unauthorized user')

@admin_api.after_request
def after_request(response):
    if response.is_json:
        data = response.get_json()
        ret = {}
        if isinstance(data, (tuple, list, set)) or not data.get('error', None):
            if('data' not in data):
                ret['data'] = data
            else:
                ret = data
            ret['meta'] = {
                'message':'response ok'
            }
        else:
            ret['meta'] = data
        return jsonify(ret)
    return response

# 400错误处理
@admin_api.errorhandler(exceptions.BadRequest)
def handle_bad_request(e):
    message = e.data and e.data['message'] or e.message
    return bad_request(message)

# 401错误处理
@admin_api.errorhandler(exceptions.Unauthorized)
def handle_unauthorized(e):
    message = '请求未认证'
    return unauthorized(message)

# 401错误处理
@admin_api.errorhandler(exceptions.Forbidden)
def handle_forbidden(e):
    message = '无访问权限'
    return forbidden(message)

# 404错误处理
@admin_api.errorhandler(exceptions.NotFound)
def handle_not_found(e):
    message = e.data and e.data['message'] or '未找到资源'
    return not_found(message)