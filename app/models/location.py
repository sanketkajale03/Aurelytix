from app.extensions import db


class Location(db.Model):
    __tablename__ = "locations"

    location_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))

    def __repr__(self) -> str:
        return f"<Location {self.city}>"
