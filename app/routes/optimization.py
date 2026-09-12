from flask import Blueprint, jsonify

optimization_bp = Blueprint("optimization", __name__)


@optimization_bp.get("/api/optimization/channels")
def optimize_channels():
    from app.machine_learning.channel_optimizer import ChannelOptimizer

    recommendations = ChannelOptimizer.optimize_all_channels()

    return jsonify({
        "total_channels": len(recommendations),
        "recommendations": recommendations,
    }), 200


@optimization_bp.get("/api/optimization/budget")
def allocate_budget():
    from flask import request

    from app.machine_learning.budget_allocator import BudgetAllocator

    budget = request.args.get(
        "budget",
        default=1000000,
        type=float,
    )

    if budget <= 0:
        return jsonify({
            "error": "Budget must be greater than 0."
        }), 400

    allocation = BudgetAllocator.allocate_budget(budget)

    return jsonify(allocation), 200

@optimization_bp.get("/api/optimization/forecast/<int:campaign_id>")
def forecast_campaign(campaign_id):
    from flask import request

    from app.machine_learning.campaign_forecaster import (
        CampaignForecaster,
    )

    days = request.args.get(
        "days",
        default=7,
        type=int,
    )

    if days <= 0 or days > 30:
        return jsonify({
            "error": "Days must be between 1 and 30."
        }), 400

    result = CampaignForecaster.forecast_campaign(
        campaign_id,
        days,
    )

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200