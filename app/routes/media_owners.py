from flask import Blueprint, jsonify, request

from app.services.media_owner_service import MediaOwnerService


media_owners_bp = Blueprint(
    "media_owners",
    __name__
)


@media_owners_bp.get("/api/media-owners")
def get_media_owners():
    """Return all media owners."""

    return jsonify(
        MediaOwnerService.get_all()
    ), 200


@media_owners_bp.get("/api/media-owners/<int:media_owner_id>")
def get_media_owner(media_owner_id):
    """Return a media owner by ID."""

    media_owner = MediaOwnerService.get_by_id(
        media_owner_id
    )

    if media_owner is None:
        return jsonify(
            {
                "error": "Media owner not found"
            }
        ), 404

    return jsonify(media_owner), 200


@media_owners_bp.post("/api/media-owners")
def create_media_owner():
    """Create a media owner."""

    data = request.get_json(
        silent=True
    ) or {}

    required_fields = [
        "media_owner_name",
        "media_owner_code",
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
        media_owner = MediaOwnerService.create(
            data
        )

        return jsonify(
            media_owner
        ), 201

    except Exception as exc:
        return jsonify(
            {
                "error": "Unable to create media owner",
                "details": str(exc),
            }
        ), 400


@media_owners_bp.put(
    "/api/media-owners/<int:media_owner_id>"
)
def update_media_owner(media_owner_id):
    """Update a media owner."""

    data = request.get_json(
        silent=True
    ) or {}

    try:
        media_owner = MediaOwnerService.update(
            media_owner_id,
            data
        )

        if media_owner is None:
            return jsonify(
                {
                    "error": "Media owner not found"
                }
            ), 404

        return jsonify(
            media_owner
        ), 200

    except Exception as exc:
        return jsonify(
            {
                "error": "Unable to update media owner",
                "details": str(exc),
            }
        ), 400


@media_owners_bp.delete(
    "/api/media-owners/<int:media_owner_id>"
)
def delete_media_owner(media_owner_id):
    """Delete a media owner."""

    deleted = MediaOwnerService.delete(
        media_owner_id
    )

    if not deleted:
        return jsonify(
            {
                "error": "Media owner not found"
            }
        ), 404

    return jsonify(
        {
            "message": "Media owner deleted successfully",
            "media_owner_id": media_owner_id,
        }
    ), 200