"""请求参数校验文件

Copyright (C) 2018 fly_lxl@foxmail.com
CreatedAt 2018-07-17
"""

from flask_restful import reqparse
from ..utils import email

# 用户检测
parser_account = reqparse.RequestParser()
parser_account.add_argument('email', required=True, trim=True, type=email, help='请输入正确的邮箱')
parser_account.add_argument('password', required=True, trim=True, help='请输入密码')

# 博文分类
parser_catalog = reqparse.RequestParser()
parser_catalog.add_argument('catalog', required=True, trim=True)

# 博文标签
parser_tag = reqparse.RequestParser()
parser_tag.add_argument('tag', required=True, trim=True)

# 博客检测
parser_post = reqparse.RequestParser()
parser_post.add_argument('title', required=True, trim=True)
parser_post.add_argument('summary', required=True, trim=True)
parser_post.add_argument('content', required=True, trim=True)
parser_post.add_argument('catalog', required=True, type=int)
parser_post.add_argument('tags', type=int, action='append')

# 分页参数
parser_pagination = reqparse.RequestParser()
parser_pagination.add_argument('offset', type=int, location='args', default=0, help='offset is the first index of item')
parser_pagination.add_argument('limit', type=int, location='args', default=10, help='limit is the max number for request')

# 评论参数
parser_comment = reqparse.RequestParser()
parser_comment.add_argument('name', required=True, trim=True)
parser_comment.add_argument('email', required=True, trim=True, type=email)
parser_comment.add_argument('content', required=True, trim=True)
parser_comment.add_argument('reply', type=int)
parser_comment.add_argument('post', type=int, required=True)
