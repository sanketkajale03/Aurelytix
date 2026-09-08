from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from app.extensions import db


class MediaOwner(db.Model):
    __tablename__ = "media_owners"

    media_owner_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    media_owner_name = db.Column(db.String(150), nullable=False)
    media_owner_code = db.Column(db.String(50), nullable=False)
    media_type = db.Column(db.String(50))
    contact_email = db.Column(db.String(255))
    status = db.Column(
        db.Enum("ACTIVE", "INACTIVE"),
        nullable=False,
        server_default="ACTIVE",
    )
    created_at = db.Column(
        TIMESTAMP(),
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    updated_at = db.Column(
        TIMESTAMP(),
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (
        db.Index("media_owner_code", "media_owner_code", unique=True),
        db.Index("idx_media_owners_type", "media_type"),
        db.Index("idx_media_owners_status", "status"),
    )

    campaigns = db.relationship(
        "Campaign",
        back_populates="media_owner",
        lazy=True,
    )
