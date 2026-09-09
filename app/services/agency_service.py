from app.extensions import db
from app.models import Agency


class AgencyService:
    """Business logic for agency management."""

    @staticmethod
    def get_all():
        """Return all agencies."""

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
        """Return a single agency."""

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
        """Create a new agency."""

        agency = Agency(
            agency_name=data["agency_name"],
            agency_code=data["agency_code"],
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
            status=data.get("status", "ACTIVE"),
        )

        db.session.add(agency)
        db.session.commit()

        return AgencyService.get_by_id(agency.agency_id)

    @staticmethod
    def update(agency_id, data):
        """Update an existing agency."""

        agency = db.session.get(Agency, agency_id)

        if agency is None:
            return None

        allowed_fields = [
            "agency_name",
            "agency_code",
            "contact_email",
            "contact_phone",
            "status",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(agency, field, data[field])

        db.session.commit()

        return AgencyService.get_by_id(agency_id)

    @staticmethod
    def delete(agency_id):
        """Delete an agency."""

        agency = db.session.get(Agency, agency_id)

        if agency is None:
            return False

        db.session.delete(agency)
        db.session.commit()

        return True
