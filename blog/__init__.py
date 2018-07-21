"""
    author: lixl
    email: fly_lxl@foxmail.com
    date: Mar 3, 2018
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
from .errors import not_found

import os

db = SQLAlchemy()
migreate = Migrate()

def create_app():
    app = Flask(__name__)
    config = os.environ.get('FLASK_APP_MODE', 'config.Config')
    app.config.from_object(config)
    db.init_app(app)
    migreate.init_app(app, db)

    # add db to shell context
    @app.shell_context_processor
    def make_shell_contex():
        return dict(db=db)

    @app.errorhandler(NotFound)
    def handler_not_found(e):
        message = '访问地址错误'
        return not_found(message)

    # include model
    from . import models
    from . import events
    # register blueprint
    from .views import home
    from .admin import admin_api
    from .posts.views import posts
    app.register_blueprint(home)
    app.register_blueprint(admin_api, url_prefix='/api/admin')
    app.register_blueprint(posts)

    return app