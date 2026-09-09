from flask import Blueprint, jsonify, request

from app.services.location_service import LocationService


locations_bp = Blueprint("locations", __name__)


@locations_bp.get("/api/locations")
def get_locations():
    locations = LocationService.get_all()

    return jsonify(locations), 200


@locations_bp.get("/api/locations/<int:location_id>")
def get_location(location_id):
    location = LocationService.get_by_id(location_id)

    if location is None:
        return jsonify({
            "error": "Location not found"
        }), 404

    return jsonify(location), 200


@locations_bp.post("/api/locations")
def create_location():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if not data.get("country"):
        return jsonify({
            "error": "Missing required field",
            "field": "country"
        }), 400

    location = LocationService.create(data)

    return jsonify(location), 201


@locations_bp.put("/api/locations/<int:location_id>")
def update_location(location_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    location = LocationService.update(
        location_id,
        data
    )

    if location is None:
        return jsonify({
            "error": "Location not found"
        }), 404

    return jsonify(location), 200


@locations_bp.delete("/api/locations/<int:location_id>")
def delete_location(location_id):
    deleted = LocationService.delete(location_id)

    if not deleted:
        return jsonify({
            "error": "Location not found"
        }), 404

    return jsonify({
        "message": "Location deleted successfully"
    }), 200