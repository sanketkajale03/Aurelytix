from app.extensions import db
from app.models import Location


def seed_locations():
    locations = [
        ("India", "Maharashtra", "Mumbai", "400001", 19.0760, 72.8777),
        ("India", "Maharashtra", "Pune", "411001", 18.5204, 73.8567),
        ("India", "Delhi", "New Delhi", "110001", 28.6139, 77.2090),
        ("India", "Karnataka", "Bengaluru", "560001", 12.9716, 77.5946),
        ("India", "Tamil Nadu", "Chennai", "600001", 13.0827, 80.2707),
        ("India", "Telangana", "Hyderabad", "500001", 17.3850, 78.4867),
        ("India", "West Bengal", "Kolkata", "700001", 22.5726, 88.3639),
        ("India", "Gujarat", "Ahmedabad", "380001", 23.0225, 72.5714),
        ("India", "Rajasthan", "Jaipur", "302001", 26.9124, 75.7873),
        ("India", "Uttar Pradesh", "Lucknow", "226001", 26.8467, 80.9462),
        ("India", "Maharashtra", "Nashik", "422001", 20.0059, 73.7797),
        ("India", "Kerala", "Kochi", "682001", 9.9312, 76.2673),
    ]

    created = 0

    for data in locations:
        existing = Location.query.filter_by(
            country=data[0],
            state=data[1],
            city=data[2],
        ).first()

        if not existing:
            db.session.add(
                Location(
                    country=data[0],
                    state=data[1],
                    city=data[2],
                    postal_code=data[3],
                    latitude=data[4],
                    longitude=data[5],
                )
            )
            created += 1

    db.session.commit()
    return created
