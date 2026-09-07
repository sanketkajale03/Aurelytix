from app.extensions import db


class Channel(db.Model):
    __tablename__ = "channels"

    channel_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    channel_name = db.Column(db.String(100), nullable=False, unique=True)
    channel_type = db.Column(
        db.Enum("DOOH", "CTV", "OTT", "MOBILE", "WEB", "SOCIAL", "AUDIO"),
        nullable=False,
    )
    status = db.Column(
        db.Enum("ACTIVE", "INACTIVE"),
        nullable=False,
        default="ACTIVE",
    )

    def __repr__(self) -> str:
        return f"<Channel {self.channel_name}>"
