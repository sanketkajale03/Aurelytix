from sqlalchemy.dialects.mysql import BIGINT, SMALLINT, TIMESTAMP
from app.extensions import db


class CampaignPerformance(db.Model):
    __tablename__ = "campaign_performance"

    performance_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    campaign_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "campaigns.campaign_id",
            name="fk_performance_campaign",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    channel_id = db.Column(
        SMALLINT(unsigned=True),
        db.ForeignKey(
            "channels.channel_id",
            name="fk_performance_channel",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    location_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "locations.location_id",
            name="fk_performance_location",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    performance_date = db.Column(
        db.Date,
        nullable=False,
    )

    impressions = db.Column(
        BIGINT(unsigned=True),
        nullable=False,
        server_default="0",
    )

    clicks = db.Column(
        BIGINT(unsigned=True),
        nullable=False,
        server_default="0",
    )

    conversions = db.Column(
        BIGINT(unsigned=True),
        nullable=False,
        server_default="0",
    )

    spend = db.Column(
        db.Numeric(15, 2),
        nullable=False,
        server_default="0.00",
    )

    revenue = db.Column(
        db.Numeric(15, 2),
        nullable=False,
        server_default="0.00",
    )

    created_at = db.Column(
        TIMESTAMP(),
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    __table_args__ = (
        db.Index(
            "fk_performance_location",
            "location_id",
        ),
        db.Index(
            "idx_performance_campaign",
            "campaign_id",
        ),
        db.Index(
            "idx_performance_channel",
            "channel_id",
        ),
        db.Index(
            "idx_performance_date",
            "performance_date",
        ),
        db.Index(
            "idx_performance_campaign_date",
            "campaign_id",
            "performance_date",
        ),
        db.CheckConstraint(
            "spend >= 0",
            name="chk_performance_spend",
        ),
        db.CheckConstraint(
            "revenue >= 0",
            name="chk_performance_revenue",
        ),
    )

    campaign = db.relationship(
        "Campaign",
        back_populates="performances",
    )

    channel = db.relationship(
        "Channel",
        back_populates="performances",
    )

    location = db.relationship(
        "Location",
        back_populates="performances",
    )
