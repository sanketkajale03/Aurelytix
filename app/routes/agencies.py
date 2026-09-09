from flask import Blueprint, jsonify, request

from app.services.agency_service import AgencyService


agencies_bp = Blueprint("agencies", __name__)


@agencies_bp.get("/api/agencies")
def get_agencies():
    """Return all agencies."""

    return jsonify(AgencyService.get_all()), 200


@agencies_bp.get("/api/agencies/<int:agency_id>")
def get_agency(agency_id):
    """Return an agency by ID."""

    agency = AgencyService.get_by_id(agency_id)

    if agency is None:
        return jsonify({"error": "Agency not found"}), 404

    return jsonify(agency), 200


@agencies_bp.post("/api/agencies")
def create_agency():
    """Create a new agency."""

    data = request.get_json(silent=True) or {}

    required_fields = [
        "agency_name",
        "agency_code",
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
        agency = AgencyService.create(data)

        return jsonify(agency), 201

    except Exception as exc:
        return jsonify(
            {
                "error": "Unable to create agency",
                "details": str(exc),
            }
        ), 400


@agencies_bp.put("/api/agencies/<int:agency_id>")
def update_agency(agency_id):
    """Update an agency."""

    data = request.get_json(silent=True) or {}

    try:
        agency = AgencyService.update(
            agency_id,
            data,
        )

        if agency is None:
            return jsonify(
                {"error": "Agency not found"}
            ), 404

        return jsonify(agency), 200

    except Exception as exc:
        return jsonify(
            {
                "error": "Unable to update agency",
                "details": str(exc),
            }
        ), 400


@agencies_bp.delete("/api/agencies/<int:agency_id>")
def delete_agency(agency_id):
    """Delete an agency."""

    deleted = AgencyService.delete(agency_id)

    if not deleted:
        return jsonify(
            {"error": "Agency not found"}
        ), 404

    return jsonify(
        {
            "message": "Agency deleted successfully",
            "agency_id": agency_id,
        }
    ), 200
