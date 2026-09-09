from flask import Blueprint, jsonify

from app.services.analytics_service import AnalyticsService


analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.get("/api/analytics/kpis")
def analytics_kpis():
    return jsonify(AnalyticsService.get_kpis()), 200

@analytics_bp.get("/api/analytics/channel-performance")
def channel_performance():
    return jsonify(AnalyticsService.get_channel_performance()), 200


@analytics_bp.get("/api/analytics/campaign-performance")
def campaign_performance():
    return jsonify(AnalyticsService.get_campaign_performance()), 200


@analytics_bp.get("/api/analytics/location-performance")
def location_performance():
    return jsonify(AnalyticsService.get_location_performance()), 200


@analytics_bp.get("/api/analytics/trends")
def performance_trends():
    return jsonify(AnalyticsService.get_daily_trends()), 200