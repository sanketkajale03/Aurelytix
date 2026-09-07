from app.extensions import db


class Advertiser(db.Model):
    __tablename__ = "advertisers"

    advertiser_id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    agency_id = db.Column(
        db.BigInteger,
        db.ForeignKey("agencies.agency_id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    advertiser_name = db.Column(
        db.String(150),
        nullable=False
    )

    advertiser_code = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    industry = db.Column(
        db.String(100),
        index=True
    )

    contact_email = db.Column(db.String(255))

    status = db.Column(
        db.Enum("ACTIVE", "INACTIVE"),
        nullable=False,
        default="ACTIVE",
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    agency = db.relationship(
        "Agency",
        back_populates="advertisers"
    )

    brands = db.relationship(
        "Brand",
        back_populates="advertiser",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Advertiser {self.advertiser_code}>"