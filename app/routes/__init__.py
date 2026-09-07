from app.routes.health import health_bp


def register_routes(app):
    """Register application blueprints."""

    app.register_blueprint(health_bp, url_prefix="/api")