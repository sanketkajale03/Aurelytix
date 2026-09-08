from flask import Flask

from config.settings import DevelopmentConfig
from app.extensions import db, migrate
from app.routes import register_routes


def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    db.init_app(flask_app)

    # Load all SQLAlchemy models before Flask-Migrate initialization.
    import app.models  # noqa: F401

    migrate.init_app(flask_app, db)

    register_routes(flask_app)

    return flask_app
