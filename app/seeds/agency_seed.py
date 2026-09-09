from app.extensions import db
from app.models import Agency


def seed_agencies():
    """Seed agency master data."""

    agencies = [
        {
            "agency_name": "Aurelia Media Group",
            "agency_code": "AMG001",
            "contact_email": "contact@aureliamedia.com",
            "contact_phone": "+91-9876543210",
        },
        {
            "agency_name": "Vertex Advertising",
            "agency_code": "VAD001",
            "contact_email": "contact@vertexads.com",
            "contact_phone": "+91-9876543211",
        },
        {
            "agency_name": "Nexa Digital Media",
            "agency_code": "NDM001",
            "contact_email": "contact@nexadigital.com",
            "contact_phone": "+91-9876543212",
        },
        {
            "agency_name": "BluePeak Marketing",
            "agency_code": "BPM001",
            "contact_email": "contact@bluepeakmarketing.com",
            "contact_phone": "+91-9876543213",
        },
        {
            "agency_name": "Orbit Media Solutions",
            "agency_code": "OMS001",
            "contact_email": "contact@orbitmedia.com",
            "contact_phone": "+91-9876543214",
        },
    ]

    created = 0

    for data in agencies:
        existing = Agency.query.filter_by(
            agency_code=data["agency_code"]
        ).first()

        if not existing:
            db.session.add(Agency(**data))
            created += 1

    db.session.commit()

    return created