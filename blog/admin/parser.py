"""请求参数校验文件

Copyright (C) 2018 fly_lxl@foxmail.com
CreatedAt 2018-07-17
"""

from flask_restful import reqparse
from ..utils import email

# 用户检测
parser_account = reqparse.RequestParser()
parser_account.add_argument('email', required=True, trim=True, type=email)
parser_account.add_argument('password', required=True, trim=True)

# 博文分类
parser_catalog = reqparse.RequestParser()
parser_catalog.add_argument('catalog', required=True, trim=True)