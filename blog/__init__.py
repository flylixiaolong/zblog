"""
    author: Xiaolong Li
    email: fly_lxl@foxmail.com
    date: Mar 3, 2018
"""

from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # register blueprint
    from .views import home
    app.register_blueprint(home)
    return app
