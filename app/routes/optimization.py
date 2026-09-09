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