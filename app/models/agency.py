from app.extensions import db


class Agency(db.Model):
    __tablename__ = "agencies"

    agency_id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    agency_name = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    agency_code = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(30))

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

    advertisers = db.relationship(
        "Advertiser",
        back_populates="agency",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Agency {self.agency_code}>"