from datetime import datetime, timezone

from flask import Blueprint, jsonify


health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    """Return application health information."""

    return jsonify(
        {
            "status": "healthy",
            "application": "Aurelytix",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )