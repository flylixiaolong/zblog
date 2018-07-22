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