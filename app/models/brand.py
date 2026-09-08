from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from app.extensions import db


class Brand(db.Model):
    __tablename__ = "brands"

    brand_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    advertiser_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "advertisers.advertiser_id",
            name="fk_brands_advertiser",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    brand_name = db.Column(db.String(150), nullable=False)
    brand_code = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100))
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
        db.Index("brand_code", "brand_code", unique=True),
        db.Index("idx_brands_advertiser", "advertiser_id"),
        db.Index("idx_brands_category", "category"),
    )

    advertiser = db.relationship(
        "Advertiser",
        back_populates="brands",
    )

    campaigns = db.relationship(
        "Campaign",
        back_populates="brand",
        lazy=True,
    )
