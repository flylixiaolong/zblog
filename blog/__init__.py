"""
    author: lixl
    email: fly_lxl@foxmail.com
    date: Mar 3, 2018
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 


import os

db = SQLAlchemy()
migreate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    config = os.environ.get('FLASK_APP_MODE', 'config.Config')
    app.config.from_object(config)
    db.init_app(app)
    migreate.init_app(app, db)
    login_manager.init_app(app)

    # add db to shell context
    @app.shell_context_processor
    def make_shell_contex():
        return dict(db=db)

    # include model
    from blog import models
    from blog import events
    # register blueprint
    from blog.views import home
    app.register_blueprint(home)

    return app