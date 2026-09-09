from app.extensions import db
from app.models import MediaOwner


def seed_media_owners():
    media_owners = [
        ("Times Network", "TN001", "DOOH"),
        ("Lamar Advertising", "LAM001", "DOOH"),
        ("Google Ads", "GA001", "WEB"),
        ("Meta Platforms", "META001", "SOCIAL"),
        ("YouTube", "YT001", "CTV"),
        ("Amazon Ads", "AMZ001", "OTT"),
        ("Spotify Advertising", "SP001", "AUDIO"),
        ("Jio Advertising", "JIO001", "OTT"),
    ]

    created = 0

    for name, code, media_type in media_owners:
        if not MediaOwner.query.filter_by(
            media_owner_code=code
        ).first():
            db.session.add(
                MediaOwner(
                    media_owner_name=name,
                    media_owner_code=code,
                    media_type=media_type,
                )
            )
            created += 1

    db.session.commit()
    return created
