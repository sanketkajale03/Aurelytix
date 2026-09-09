from app.extensions import db
from app.models import Advertiser


class AdvertiserService:

    @staticmethod
    def get_all():
        advertisers = Advertiser.query.order_by(
            Advertiser.created_at.desc()
        ).all()

        return [
            {
                "advertiser_id": advertiser.advertiser_id,
                "agency_id": advertiser.agency_id,
                "advertiser_name": advertiser.advertiser_name,
                "advertiser_code": advertiser.advertiser_code,
                "industry": advertiser.industry,
                "contact_email": advertiser.contact_email,
                "status": advertiser.status,
            }
            for advertiser in advertisers
        ]

    @staticmethod
    def get_by_id(advertiser_id):
        advertiser = db.session.get(Advertiser, advertiser_id)

        if advertiser is None:
            return None

        return {
            "advertiser_id": advertiser.advertiser_id,
            "agency_id": advertiser.agency_id,
            "advertiser_name": advertiser.advertiser_name,
            "advertiser_code": advertiser.advertiser_code,
            "industry": advertiser.industry,
            "contact_email": advertiser.contact_email,
            "status": advertiser.status,
        }

    @staticmethod
    def create(data):
        advertiser = Advertiser(
            agency_id=data.get("agency_id"),
            advertiser_name=data["advertiser_name"],
            advertiser_code=data["advertiser_code"],
            industry=data.get("industry"),
            contact_email=data.get("contact_email"),
            status=data.get("status", "ACTIVE"),
        )

        db.session.add(advertiser)
        db.session.commit()

        return AdvertiserService.get_by_id(advertiser.advertiser_id)

    @staticmethod
    def update(advertiser_id, data):
        advertiser = db.session.get(Advertiser, advertiser_id)

        if advertiser is None:
            return None

        allowed_fields = [
            "agency_id",
            "advertiser_name",
            "advertiser_code",
            "industry",
            "contact_email",
            "status",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(advertiser, field, data[field])

        db.session.commit()

        return AdvertiserService.get_by_id(advertiser_id)

    @staticmethod
    def delete(advertiser_id):
        advertiser = db.session.get(Advertiser, advertiser_id)

        if advertiser is None:
            return False

        db.session.delete(advertiser)
        db.session.commit()

        return True