from app.routes.health import health_bp
from app.routes.dashboard import dashboard_bp


def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def home():
        return {
            "application": "Aurelytix",
            "status": "Running",
            "version": "1.0.0"
        }
