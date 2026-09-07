from app.extensions import db


class CampaignPerformance(db.Model):
    __tablename__ = "campaign_performance"

    performance_id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )

    campaign_id = db.Column(
        db.BigInteger,
        db.ForeignKey("campaigns.campaign_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    channel_id = db.Column(
        db.SmallInteger,
        db.ForeignKey("channels.channel_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    location_id = db.Column(
        db.BigInteger,
        db.ForeignKey("locations.location_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    performance_date = db.Column(db.Date, nullable=False, index=True)

    impressions = db.Column(db.BigInteger, nullable=False, default=0)
    clicks = db.Column(db.BigInteger, nullable=False, default=0)
    conversions = db.Column(db.BigInteger, nullable=False, default=0)

    spend = db.Column(db.Numeric(15, 2), nullable=False, default=0)
    revenue = db.Column(db.Numeric(15, 2), nullable=False, default=0)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )

    campaign = db.relationship("Campaign")
    channel = db.relationship("Channel")
    location = db.relationship("Location")

    def __repr__(self) -> str:
        return f"<CampaignPerformance {self.performance_id}>"
