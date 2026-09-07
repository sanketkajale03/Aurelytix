from app.extensions import db


class Brand(db.Model):
    __tablename__ = "brands"

    brand_id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    advertiser_id = db.Column(
        db.BigInteger,
        db.ForeignKey(
            "advertisers.advertiser_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    brand_name = db.Column(
        db.String(150),
        nullable=False
    )

    brand_code = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String(100),
        index=True
    )

    status = db.Column(
        db.Enum("ACTIVE", "INACTIVE"),
        nullable=False,
        default="ACTIVE"
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

    advertiser = db.relationship(
        "Advertiser",
        back_populates="brands"
    )

    campaigns = db.relationship(
        "Campaign",
        back_populates="brand",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Brand {self.brand_code}>"