from flask import Blueprint, jsonify, request

from app.services.agency_service import AgencyService

agencies_bp = Blueprint(
    "agencies",
    __name__,
)


@agencies_bp.get("/api/agencies")
def get_agencies():
    return jsonify(
        AgencyService.get_all()
    )


@agencies_bp.get("/api/agencies/<int:agency_id>")
def get_agency(agency_id):

    agency = AgencyService.get_by_id(
        agency_id
    )

    if agency is None:
        return jsonify(
            {
                "error": "Agency not found"
            }
        ), 404

    return jsonify(agency)


@agencies_bp.post("/api/agencies")
def create_agency():

    data = request.get_json()

    agency = AgencyService.create(data)

    return jsonify(agency), 201


@agencies_bp.put("/api/agencies/<int:agency_id>")
def update_agency(agency_id):

    data = request.get_json()

    agency = AgencyService.update(
        agency_id,
        data,
    )

    if agency is None:
        return jsonify(
            {
                "error": "Agency not found"
            }
        ), 404

    return jsonify(agency)


@agencies_bp.delete("/api/agencies/<int:agency_id>")
def delete_agency(agency_id):

    deleted = AgencyService.delete(
        agency_id
    )

    if not deleted:
        return jsonify(
            {
                "error": "Agency not found"
            }
        ), 404

    return jsonify(
        {
            "message": "Agency deleted successfully"
        }
    )