from flask import Flask

from config.settings import DevelopmentConfig
from app.extensions import db, migrate
from app.routes import register_routes
from app.utils.logger import configure_logging


def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application."""

    configure_logging()

    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)

    return app