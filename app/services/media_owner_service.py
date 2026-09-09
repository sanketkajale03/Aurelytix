from app.extensions import db
from app.models import MediaOwner


class MediaOwnerService:
    """Business logic for media owner management."""

    @staticmethod
    def get_all():
        """Return all media owners."""

        media_owners = MediaOwner.query.order_by(
            MediaOwner.created_at.desc()
        ).all()

        return [
            {
                "media_owner_id": media_owner.media_owner_id,
                "media_owner_name": media_owner.media_owner_name,
                "media_owner_code": media_owner.media_owner_code,
                "media_type": media_owner.media_type,
                "contact_email": media_owner.contact_email,
                "status": media_owner.status,
            }
            for media_owner in media_owners
        ]

    @staticmethod
    def get_by_id(media_owner_id):
        """Return a single media owner."""

        media_owner = db.session.get(
            MediaOwner,
            media_owner_id
        )

        if media_owner is None:
            return None

        return {
            "media_owner_id": media_owner.media_owner_id,
            "media_owner_name": media_owner.media_owner_name,
            "media_owner_code": media_owner.media_owner_code,
            "media_type": media_owner.media_type,
            "contact_email": media_owner.contact_email,
            "status": media_owner.status,
        }

    @staticmethod
    def create(data):
        """Create a new media owner."""

        media_owner = MediaOwner(
            media_owner_name=data["media_owner_name"],
            media_owner_code=data["media_owner_code"],
            media_type=data.get("media_type"),
            contact_email=data.get("contact_email"),
            status=data.get("status", "ACTIVE"),
        )

        db.session.add(media_owner)
        db.session.commit()

        return MediaOwnerService.get_by_id(
            media_owner.media_owner_id
        )

    @staticmethod
    def update(media_owner_id, data):
        """Update an existing media owner."""

        media_owner = db.session.get(
            MediaOwner,
            media_owner_id
        )

        if media_owner is None:
            return None

        allowed_fields = [
            "media_owner_name",
            "media_owner_code",
            "media_type",
            "contact_email",
            "status",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(
                    media_owner,
                    field,
                    data[field]
                )

        db.session.commit()

        return MediaOwnerService.get_by_id(
            media_owner_id
        )

    @staticmethod
    def delete(media_owner_id):
        """Delete a media owner."""

        media_owner = db.session.get(
            MediaOwner,
            media_owner_id
        )

        if media_owner is None:
            return False

        db.session.delete(media_owner)
        db.session.commit()

        return True