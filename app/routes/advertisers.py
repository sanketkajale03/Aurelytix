from flask import Blueprint, jsonify, request

from app.services.advertiser_service import AdvertiserService


advertisers_bp = Blueprint("advertisers", __name__)


@advertisers_bp.get("/api/advertisers")
def get_advertisers():
    advertisers = AdvertiserService.get_all()
    return jsonify(advertisers), 200


@advertisers_bp.get("/api/advertisers/<int:advertiser_id>")
def get_advertiser(advertiser_id):
    advertiser = AdvertiserService.get_by_id(advertiser_id)

    if advertiser is None:
        return jsonify({
            "error": "Advertiser not found"
        }), 404

    return jsonify(advertiser), 200


@advertisers_bp.post("/api/advertisers")
def create_advertiser():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "advertiser_name",
        "advertiser_code",
    ]

    missing_fields = [
        field for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    advertiser = AdvertiserService.create(data)

    return jsonify(advertiser), 201


@advertisers_bp.put("/api/advertisers/<int:advertiser_id>")
def update_advertiser(advertiser_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    advertiser = AdvertiserService.update(
        advertiser_id,
        data
    )

    if advertiser is None:
        return jsonify({
            "error": "Advertiser not found"
        }), 404

    return jsonify(advertiser), 200


@advertisers_bp.delete("/api/advertisers/<int:advertiser_id>")
def delete_advertiser(advertiser_id):
    deleted = AdvertiserService.delete(advertiser_id)

    if not deleted:
        return jsonify({
            "error": "Advertiser not found"
        }), 404

    return jsonify({
        "message": "Advertiser deleted successfully"
    }), 200