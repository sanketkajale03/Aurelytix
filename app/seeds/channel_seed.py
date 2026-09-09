from app.extensions import db
from app.models import Channel


def seed_channels():
    channels = [
        ("Digital Out-of-Home", "DOOH"),
        ("Connected TV", "CTV"),
        ("Over-the-Top", "OTT"),
        ("Mobile Advertising", "MOBILE"),
        ("Web Advertising", "WEB"),
        ("Social Media", "SOCIAL"),
        ("Digital Audio", "AUDIO"),
    ]

    created = 0

    for name, channel_type in channels:
        if not Channel.query.filter_by(channel_name=name).first():
            db.session.add(
                Channel(
                    channel_name=name,
                    channel_type=channel_type,
                )
            )
            created += 1

    db.session.commit()
    return created
