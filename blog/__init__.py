"""
    author: Xiaolong Li
    email: fly_lxl@foxmail.com
    date: Mar 3, 2018
"""

from flask import Flask

import os


def create_app():
    app = Flask(__name__)
    config = os.environ.get('FLASK_APP_MODE', 'config.Config')
    app.config.from_object(config)

    # register blueprint
    from .views import home
    app.register_blueprint(home)

    return app