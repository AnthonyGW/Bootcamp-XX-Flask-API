# /app/__init__.py
"""App module functions and imports
"""

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#local imports
from instance.config import app_config

#initializing sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    """Create new Flask object and
    connect to database
    """
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
