from app.extensions import db
from app.models import Advertiser, Brand


def seed_brands():
    brand_data = [
        ("GMI001", "Velocity Motors", "VM001", "Automotive"),
        ("GMI001", "DriveMax", "DM001", "Automotive"),
        ("NTL001", "Nova Connect", "NC001", "Telecom"),
        ("NTL001", "Nova Fiber", "NF001", "Telecom"),
        ("FMR001", "FreshMart", "FM001", "Retail"),
        ("FMR001", "DailyChoice", "DC001", "Retail"),
        ("ZFN001", "Zenith Bank", "ZB001", "Banking"),
        ("ZFN001", "Zenith Invest", "ZI001", "Investment"),
        ("USF001", "UrbanStyle", "US001", "Fashion"),
        ("USF001", "UrbanFit", "UF001", "Fashion"),
        ("HPL001", "HealthPlus", "HP001", "Healthcare"),
        ("SKH001", "Skyline Hotels", "SH001", "Hospitality"),
        ("TNS001", "TechNova", "TN001", "Technology"),
        ("GLF001", "GreenLife", "GL001", "Food"),
        ("RWM001", "RideWave", "RW001", "Mobility"),
    ]

    created = 0

    for advertiser_code, name, code, category in brand_data:
        advertiser = Advertiser.query.filter_by(
            advertiser_code=advertiser_code
        ).first()

        if advertiser and not Brand.query.filter_by(
            brand_code=code
        ).first():
            db.session.add(
                Brand(
                    advertiser_id=advertiser.advertiser_id,
                    brand_name=name,
                    brand_code=code,
                    category=category,
                )
            )
            created += 1

    db.session.commit()
    return created
