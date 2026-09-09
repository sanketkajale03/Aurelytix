from flask import Blueprint, jsonify

from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    data = DashboardService.get_dashboard()
    return jsonify(data), 200
