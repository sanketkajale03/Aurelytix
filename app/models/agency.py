from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from app.extensions import db


class Agency(db.Model):
    __tablename__ = "agencies"

    agency_id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    agency_name = db.Column(db.String(150), nullable=False)
    agency_code = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(30))
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
        db.Index("agency_code", "agency_code", unique=True),
        db.Index("idx_agencies_status", "status"),
        db.Index("idx_agencies_name", "agency_name"),
    )

    advertisers = db.relationship(
        "Advertiser",
        back_populates="agency",
        lazy=True,
    )
