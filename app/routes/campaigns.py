from datetime import date

from flask import Blueprint, jsonify, request

from app.services.campaign_service import CampaignService


campaigns_bp = Blueprint("campaigns", __name__)


@campaigns_bp.get("/api/campaigns")
def get_campaigns():
    """Return all campaigns."""
    return jsonify(CampaignService.get_all()), 200


@campaigns_bp.get("/api/campaigns/<int:campaign_id>")
def get_campaign(campaign_id):
    """Return a campaign by ID."""

    campaign = CampaignService.get_by_id(campaign_id)

    if campaign is None:
        return jsonify({"error": "Campaign not found"}), 404

    return jsonify(campaign), 200


@campaigns_bp.post("/api/campaigns")
def create_campaign():
    """Create a campaign."""

    data = request.get_json(silent=True) or {}

    required_fields = [
        "brand_id",
        "campaign_name",
        "campaign_code",
        "start_date",
        "end_date",
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify(
            {
                "error": "Missing required fields",
                "fields": missing,
            }
        ), 400

    try:
        data["start_date"] = date.fromisoformat(
            data["start_date"]
        )

        data["end_date"] = date.fromisoformat(
            data["end_date"]
        )

        campaign = CampaignService.create(data)

        return jsonify(campaign), 201

    except Exception as exc:
        return jsonify(
            {
                "error": "Unable to create campaign",
                "details": str(exc),
            }
        ), 400


@campaigns_bp.put("/api/campaigns/<int:campaign_id>")
def update_campaign(campaign_id):
    """Update a campaign."""

    data = request.get_json(silent=True) or {}

    if "start_date" in data:
        data["start_date"] = date.fromisoformat(
            data["start_date"]
        )

    if "end_date" in data:
        data["end_date"] = date.fromisoformat(
            data["end_date"]
        )

    campaign = CampaignService.update(
        campaign_id,
        data,
    )

    if campaign is None:
        return jsonify({"error": "Campaign not found"}), 404

    return jsonify(campaign), 200


@campaigns_bp.delete("/api/campaigns/<int:campaign_id>")
def delete_campaign(campaign_id):
    """Delete a campaign."""

    deleted = CampaignService.delete(campaign_id)

    if not deleted:
        return jsonify({"error": "Campaign not found"}), 404

    return jsonify(
        {
            "message": "Campaign deleted successfully",
            "campaign_id": campaign_id,
        }
    ), 200