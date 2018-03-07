"""
    create flask app.
"""

from blog import create_app
import config

app = create_app(config.Config)

