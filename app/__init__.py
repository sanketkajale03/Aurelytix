from pathlib import Path

from flask import Flask

from config.settings import DevelopmentConfig
from app.extensions import db, migrate
from app.routes import register_routes


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application."""

    flask_app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    flask_app.config.from_object(config_class)

    db.init_app(flask_app)

    # Load all SQLAlchemy models before Flask-Migrate initialization.
    import app.models  # noqa: F401

    migrate.init_app(flask_app, db)

    register_routes(flask_app)

    return flask_app