from app.routes.analytics import analytics_bp
from app.routes.campaigns import campaigns_bp
from app.routes.dashboard import dashboard_bp
from app.routes.health import health_bp
from app.routes.agencies import agencies_bp
from app.routes.brands import brands_bp
from app.routes.media_owners import media_owners_bp
from app.routes.advertisers import advertisers_bp
from app.routes.audiences import audiences_bp
from app.routes.locations import locations_bp
from app.routes.optimization import optimization_bp


def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(agencies_bp)
    app.register_blueprint(brands_bp)
    app.register_blueprint(media_owners_bp)
    app.register_blueprint(advertisers_bp)
    app.register_blueprint(audiences_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(optimization_bp)
    @app.route("/")
    def home():
        return {
            "application": "Aurelytix",
            "status": "Running",
            "version": "1.0.0",
        }