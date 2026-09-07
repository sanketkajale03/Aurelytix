from app.extensions import db


class AudienceSegment(db.Model):
    __tablename__ = "audience_segments"

    audience_segment_id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )
    segment_name = db.Column(db.String(150), nullable=False, unique=True)
    age_min = db.Column(db.SmallInteger)
    age_max = db.Column(db.SmallInteger)
    gender = db.Column(
        db.Enum("MALE", "FEMALE", "ALL"),
        nullable=False,
        default="ALL",
    )
    income_level = db.Column(db.String(50))
    interests = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"<AudienceSegment {self.segment_name}>"
