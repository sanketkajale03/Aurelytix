from flask import Blueprint, jsonify, request

from app.services.audience_service import AudienceService


audiences_bp = Blueprint("audiences", __name__)


@audiences_bp.get("/api/audiences")
def get_audiences():
    audiences = AudienceService.get_all()

    return jsonify(audiences), 200


@audiences_bp.get("/api/audiences/<int:audience_segment_id>")
def get_audience(audience_segment_id):
    audience = AudienceService.get_by_id(
        audience_segment_id
    )

    if audience is None:
        return jsonify({
            "error": "Audience segment not found"
        }), 404

    return jsonify(audience), 200


@audiences_bp.post("/api/audiences")
def create_audience():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if not data.get("segment_name"):
        return jsonify({
            "error": "Missing required field",
            "field": "segment_name"
        }), 400

    audience = AudienceService.create(data)

    return jsonify(audience), 201


@audiences_bp.put("/api/audiences/<int:audience_segment_id>")
def update_audience(audience_segment_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    audience = AudienceService.update(
        audience_segment_id,
        data
    )

    if audience is None:
        return jsonify({
            "error": "Audience segment not found"
        }), 404

    return jsonify(audience), 200


@audiences_bp.delete("/api/audiences/<int:audience_segment_id>")
def delete_audience(audience_segment_id):
    deleted = AudienceService.delete(
        audience_segment_id
    )

    if not deleted:
        return jsonify({
            "error": "Audience segment not found"
        }), 404

    return jsonify({
        "message": "Audience segment deleted successfully"
    }), 200