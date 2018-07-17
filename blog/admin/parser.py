"""请求参数校验文件

Copyright (C) 2018 fly_lxl@foxmail.com
CreatedAt 2018-07-17
"""

from flask_restful import reqparse

parser_catalog = reqparse.RequestParser()
parser_catalog.add_argument('catalog', required=True, trim=True)