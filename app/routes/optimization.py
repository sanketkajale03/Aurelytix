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

@optimization_bp.get("/api/optimization/channels")
def optimize_channels():
    from app.machine_learning.channel_optimizer import ChannelOptimizer

    recommendations = ChannelOptimizer.optimize_all_channels()

    return jsonify({
        "total_channels": len(recommendations),
        "recommendations": recommendations,
    }), 200