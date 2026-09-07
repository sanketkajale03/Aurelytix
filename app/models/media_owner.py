from app.extensions import db


class MediaOwner(db.Model):
    __tablename__ = "media_owners"

    media_owner_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    media_owner_name = db.Column(db.String(150), nullable=False)
    media_owner_code = db.Column(db.String(50), nullable=False, unique=True)
    media_type = db.Column(db.String(100))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(30))
    status = db.Column(
        db.Enum("ACTIVE", "INACTIVE"),
        nullable=False,
        default="ACTIVE",
    )
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    campaigns = db.relationship("Campaign", back_populates="media_owner")

    def __repr__(self) -> str:
        return f"<MediaOwner {self.media_owner_code}>"
