from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from app.extensions import db


class Location(db.Model):
    __tablename__ = "locations"

    location_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))
    created_at = db.Column(
        TIMESTAMP(),
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    __table_args__ = (
        db.Index("idx_locations_country", "country"),
        db.Index("idx_locations_state", "state"),
        db.Index("idx_locations_city", "city"),
        db.Index(
            "idx_locations_coordinates",
            "latitude",
            "longitude",
        ),
    )

    performances = db.relationship(
        "CampaignPerformance",
        back_populates="location",
        lazy=True,
    )
