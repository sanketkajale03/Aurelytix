from flask import Blueprint, jsonify, render_template

from app.services.dashboard_service import DashboardService


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
def dashboard_home():
    """Render the Aurelytix analytics dashboard."""
    return render_template("dashboard/index.html")


@dashboard_bp.get("/api/dashboard")
def get_dashboard():
    """Return dashboard KPI data."""
    data = DashboardService.get_dashboard()
    return jsonify(data), 200