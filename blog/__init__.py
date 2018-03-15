"""
    author: Xiaolong Li
    email: fly_lxl@foxmail.com
    date: Mar 3, 2018
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

    # register blueprint
    from .views import home
    app.register_blueprint(home)

    return app