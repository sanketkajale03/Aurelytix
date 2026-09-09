from app.extensions import db
from app.models import AudienceSegment


def seed_audiences():
    audiences = [
        ("Young Professionals", 22, 35, "ALL", "MEDIUM", "Technology,Travel,Fitness"),
        ("Affluent Professionals", 30, 50, "ALL", "HIGH", "Finance,Luxury,Travel"),
        ("Gen Z Digital", 18, 27, "ALL", "MEDIUM", "Gaming,Music,Technology"),
        ("Family Decision Makers", 30, 55, "ALL", "MEDIUM", "Family,Shopping,Food"),
        ("Urban Millennials", 25, 40, "ALL", "MEDIUM", "Fashion,Travel,Entertainment"),
        ("Automotive Enthusiasts", 25, 50, "MALE", "HIGH", "Cars,Technology,Travel"),
        ("Health Conscious", 20, 55, "ALL", "MEDIUM", "Fitness,Health,Wellness"),
        ("Luxury Consumers", 30, 60, "ALL", "HIGH", "Luxury,Fashion,Travel"),
    ]

    created = 0

    for data in audiences:
        if not AudienceSegment.query.filter_by(
            segment_name=data[0]
        ).first():
            db.session.add(
                AudienceSegment(
                    segment_name=data[0],
                    age_min=data[1],
                    age_max=data[2],
                    gender=data[3],
                    income_level=data[4],
                    interests=data[5],
                )
            )
            created += 1

    db.session.commit()
    return created
