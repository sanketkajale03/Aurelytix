from app.routes.analytics import analytics_bp
from app.routes.campaigns import campaigns_bp
from app.routes.dashboard import dashboard_bp
from app.routes.health import health_bp
from app.routes.agencies import agencies_bp
from app.routes.brands import brands_bp


def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(agencies_bp)
    app.register_blueprint(brands_bp)
    @app.route("/")
    def home():
        return {
            "application": "Aurelytix",
            "status": "Running",
            "version": "1.0.0",
        }