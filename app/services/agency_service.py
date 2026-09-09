from app.extensions import db
from app.models import Agency


class AgencyService:
    """Business logic for agency management."""

    @staticmethod
    def get_all():
        agencies = Agency.query.order_by(
            Agency.created_at.desc()
        ).all()

        return [
            {
                "agency_id": agency.agency_id,
                "agency_name": agency.agency_name,
                "agency_code": agency.agency_code,
                "contact_email": agency.contact_email,
                "contact_phone": agency.contact_phone,
                "status": agency.status,
            }
            for agency in agencies
        ]

    @staticmethod
    def get_by_id(agency_id):
        agency = db.session.get(Agency, agency_id)

        if agency is None:
            return None

        return {
            "agency_id": agency.agency_id,
            "agency_name": agency.agency_name,
            "agency_code": agency.agency_code,
            "contact_email": agency.contact_email,
            "contact_phone": agency.contact_phone,
            "status": agency.status,
        }

    @staticmethod
    def create(data):

        agency = Agency(
            agency_name=data["agency_name"],
            agency_code=data["agency_code"],
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
            status=data.get("status", "ACTIVE"),
        )

        db.session.add(agency)
        db.session.commit()

        return AgencyService.get_by_id(
            agency.agency_id
        )

    @staticmethod
    def update(agency_id, data):

        agency = db.session.get(
            Agency,
            agency_id,
        )

        if agency is None:
            return None

        if "agency_name" in data:
            agency.agency_name = data["agency_name"]

        if "agency_code" in data:
            agency.agency_code = data["agency_code"]

        if "contact_email" in data:
            agency.contact_email = data["contact_email"]

        if "contact_phone" in data:
            agency.contact_phone = data["contact_phone"]

        if "status" in data:
            agency.status = data["status"]

        db.session.commit()

        return AgencyService.get_by_id(
            agency_id
        )

    @staticmethod
    def delete(agency_id):

        agency = db.session.get(
            Agency,
            agency_id,
        )

        if agency is None:
            return False

        db.session.delete(agency)
        db.session.commit()

        return True