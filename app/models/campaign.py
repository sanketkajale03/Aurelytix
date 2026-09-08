from sqlalchemy.dialects.mysql import BIGINT, SMALLINT, TIMESTAMP
from app.extensions import db


campaign_channels = db.Table(
    "campaign_channels",
    db.Column(
        "campaign_id",
        BIGINT(unsigned=True),
        db.ForeignKey(
            "campaigns.campaign_id",
            name="fk_campaign_channels_campaign",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    ),
    db.Column(
        "channel_id",
        SMALLINT(unsigned=True),
        db.ForeignKey(
            "channels.channel_id",
            name="fk_campaign_channels_channel",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        primary_key=True,
    ),
    db.Column(
        "allocated_budget",
        db.Numeric(15, 2),
        nullable=False,
        server_default="0.00",
    ),
    db.CheckConstraint(
        "allocated_budget >= 0",
        name="chk_allocated_budget",
    ),
)


campaign_locations = db.Table(
    "campaign_locations",
    db.Column(
        "campaign_id",
        BIGINT(unsigned=True),
        db.ForeignKey(
            "campaigns.campaign_id",
            name="fk_campaign_locations_campaign",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    ),
    db.Column(
        "location_id",
        BIGINT(unsigned=True),
        db.ForeignKey(
            "locations.location_id",
            name="fk_campaign_locations_location",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        primary_key=True,
    ),
)


campaign_audiences = db.Table(
    "campaign_audiences",
    db.Column(
        "campaign_id",
        BIGINT(unsigned=True),
        db.ForeignKey(
            "campaigns.campaign_id",
            name="fk_campaign_audiences_campaign",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    ),
    db.Column(
        "audience_segment_id",
        BIGINT(unsigned=True),
        db.ForeignKey(
            "audience_segments.audience_segment_id",
            name="fk_campaign_audiences_segment",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        primary_key=True,
    ),
)


class Campaign(db.Model):
    __tablename__ = "campaigns"

    campaign_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    brand_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "brands.brand_id",
            name="fk_campaigns_brand",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    media_owner_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "media_owners.media_owner_id",
            name="fk_campaigns_media_owner",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    campaign_name = db.Column(
        db.String(200),
        nullable=False,
    )

    campaign_code = db.Column(
        db.String(50),
        nullable=False,
    )

    objective = db.Column(
        db.String(100),
    )

    start_date = db.Column(
        db.Date,
        nullable=False,
    )

    end_date = db.Column(
        db.Date,
        nullable=False,
    )

    budget = db.Column(
        db.Numeric(15, 2),
        nullable=False,
        server_default="0.00",
    )

    status = db.Column(
        db.Enum(
            "DRAFT",
            "SCHEDULED",
            "ACTIVE",
            "PAUSED",
            "COMPLETED",
            "CANCELLED",
        ),
        nullable=False,
        server_default="DRAFT",
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
        db.Index("campaign_code", "campaign_code", unique=True),
        db.Index("idx_campaigns_brand", "brand_id"),
        db.Index("idx_campaigns_media_owner", "media_owner_id"),
        db.Index("idx_campaigns_status", "status"),
        db.Index(
            "idx_campaigns_dates",
            "start_date",
            "end_date",
        ),
        db.CheckConstraint(
            "budget >= 0",
            name="chk_campaign_budget",
        ),
        db.CheckConstraint(
            "end_date >= start_date",
            name="chk_campaign_dates",
        ),
    )

    brand = db.relationship(
        "Brand",
        back_populates="campaigns",
    )

    media_owner = db.relationship(
        "MediaOwner",
        back_populates="campaigns",
    )

    performances = db.relationship(
        "CampaignPerformance",
        back_populates="campaign",
        lazy=True,
    )

    channels = db.relationship(
        "Channel",
        secondary=campaign_channels,
        lazy="select",
    )

    locations = db.relationship(
        "Location",
        secondary=campaign_locations,
        lazy="select",
    )

    audience_segments = db.relationship(
        "AudienceSegment",
        secondary=campaign_audiences,
        lazy="select",
    )
