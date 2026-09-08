from sqlalchemy.dialects.mysql import SMALLINT, TIMESTAMP
from app.extensions import db


class Channel(db.Model):
    __tablename__ = "channels"

    channel_id = db.Column(
        SMALLINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    channel_name = db.Column(db.String(100), nullable=False)
    channel_type = db.Column(
        db.Enum(
            "DOOH",
            "CTV",
            "OTT",
            "MOBILE",
            "WEB",
            "SOCIAL",
            "AUDIO",
        ),
        nullable=False,
    )
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

    __table_args__ = (
        db.Index("channel_name", "channel_name", unique=True),
    )

    performances = db.relationship(
        "CampaignPerformance",
        back_populates="channel",
        lazy=True,
    )
