from app.extensions import db


class Campaign(db.Model):
    __tablename__ = "campaigns"

    campaign_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    brand_id = db.Column(
        db.BigInteger,
        db.ForeignKey("brands.brand_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    media_owner_id = db.Column(
        db.BigInteger,
        db.ForeignKey("media_owners.media_owner_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    campaign_name = db.Column(db.String(200), nullable=False)
    campaign_code = db.Column(db.String(50), nullable=False, unique=True)
    objective = db.Column(db.String(150))

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    budget = db.Column(db.Numeric(15, 2), nullable=False, default=0)

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
        default="DRAFT",
        index=True,
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

    brand = db.relationship("Brand", back_populates="campaigns")
    media_owner = db.relationship("MediaOwner", back_populates="campaigns")

    def __repr__(self) -> str:
        return f"<Campaign {self.campaign_code}>"
