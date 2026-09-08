from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from app.extensions import db


class Advertiser(db.Model):
    __tablename__ = "advertisers"

    advertiser_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    agency_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "agencies.agency_id",
            name="fk_advertisers_agency",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )
    advertiser_name = db.Column(db.String(150), nullable=False)
    advertiser_code = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(100))
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
        db.Index("advertiser_code", "advertiser_code", unique=True),
        db.Index("idx_advertisers_agency", "agency_id"),
        db.Index("idx_advertisers_industry", "industry"),
        db.Index("idx_advertisers_status", "status"),
    )

    agency = db.relationship(
        "Agency",
        back_populates="advertisers",
    )

    brands = db.relationship(
        "Brand",
        back_populates="advertiser",
        lazy=True,
    )
