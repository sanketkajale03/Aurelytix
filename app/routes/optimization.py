from flask import Blueprint, jsonify

from app.machine_learning.campaign_optimizer import (
    CampaignOptimizer,
)


optimization_bp = Blueprint(
    "optimization",
    __name__
)


@optimization_bp.get("/api/optimization/campaigns")
def optimize_campaigns():
    recommendations = (
        CampaignOptimizer.optimize_all_campaigns()
    )

    return jsonify({
        "total_campaigns": len(recommendations),
        "recommendations": recommendations,
    }), 200