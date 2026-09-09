from app.extensions import db
from app.models import Location


class LocationService:

    @staticmethod
    def get_all():
        locations = Location.query.order_by(
            Location.created_at.desc()
        ).all()

        return [
            {
                "location_id": location.location_id,
                "country": location.country,
                "state": location.state,
                "city": location.city,
                "postal_code": location.postal_code,
                "latitude": float(location.latitude)
                if location.latitude is not None else None,
                "longitude": float(location.longitude)
                if location.longitude is not None else None,
            }
            for location in locations
        ]

    @staticmethod
    def get_by_id(location_id):
        location = db.session.get(Location, location_id)

        if location is None:
            return None

        return {
            "location_id": location.location_id,
            "country": location.country,
            "state": location.state,
            "city": location.city,
            "postal_code": location.postal_code,
            "latitude": float(location.latitude)
            if location.latitude is not None else None,
            "longitude": float(location.longitude)
            if location.longitude is not None else None,
        }

    @staticmethod
    def create(data):
        location = Location(
            country=data["country"],
            state=data.get("state"),
            city=data.get("city"),
            postal_code=data.get("postal_code"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )

        db.session.add(location)
        db.session.commit()

        return LocationService.get_by_id(location.location_id)

    @staticmethod
    def update(location_id, data):
        location = db.session.get(Location, location_id)

        if location is None:
            return None

        allowed_fields = [
            "country",
            "state",
            "city",
            "postal_code",
            "latitude",
            "longitude",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(location, field, data[field])

        db.session.commit()

        return LocationService.get_by_id(location_id)

    @staticmethod
    def delete(location_id):
        location = db.session.get(Location, location_id)

        if location is None:
            return False

        db.session.delete(location)
        db.session.commit()

        return True