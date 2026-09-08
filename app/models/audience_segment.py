from sqlalchemy.dialects.mysql import BIGINT, TINYINT, TIMESTAMP
from app.extensions import db


class AudienceSegment(db.Model):
    __tablename__ = "audience_segments"

    audience_segment_id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    segment_name = db.Column(db.String(150), nullable=False)
    age_min = db.Column(TINYINT(unsigned=True))
    age_max = db.Column(TINYINT(unsigned=True))
    gender = db.Column(
        db.Enum("MALE", "FEMALE", "ALL"),
    )
    income_level = db.Column(db.String(50))
    interests = db.Column(db.String(500))
    segment_description = db.Column(db.Text)
    created_at = db.Column(
        TIMESTAMP(),
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    __table_args__ = (
        db.Index("idx_audience_gender", "gender"),
        db.Index("idx_audience_income", "income_level"),
    )
