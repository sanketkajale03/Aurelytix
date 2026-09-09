from app.extensions import db
from app.models import Agency, Advertiser


def seed_advertisers():
    advertisers = [
        ("Global Motors India", "GMI001", "Automotive"),
        ("Nova Telecom", "NTL001", "Telecommunications"),
        ("FreshMart Retail", "FMR001", "Retail"),
        ("Zenith Finance", "ZFN001", "Financial Services"),
        ("UrbanStyle Fashion", "USF001", "Fashion"),
        ("HealthPlus", "HPL001", "Healthcare"),
        ("Skyline Hotels", "SKH001", "Hospitality"),
        ("TechNova Solutions", "TNS001", "Technology"),
        ("GreenLife Foods", "GLF001", "Food & Beverage"),
        ("RideWave Mobility", "RWM001", "Transportation"),
    ]

    agencies = Agency.query.all()

    created = 0

    for i, (name, code, industry) in enumerate(advertisers):
        if not Advertiser.query.filter_by(advertiser_code=code).first():
            agency = agencies[i % len(agencies)]

            db.session.add(
                Advertiser(
                    agency_id=agency.agency_id,
                    advertiser_name=name,
                    advertiser_code=code,
                    industry=industry,
                )
            )
            created += 1

    db.session.commit()
    return created
