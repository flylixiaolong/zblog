"""Blog admin module.

Copyright (C) 2018 fly_lxl@foxmail.com
CreatedAt 2018-07-07
"""
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

admin_api = Blueprint('admin_api', __name__, url_prefix='/api/admin', template_folder='templates')
admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

CORS(admin_api)
rest_api = Api(api, catch_all_404s=True)
print(admin_api.root_path)

from . import authentication, views, errors, api