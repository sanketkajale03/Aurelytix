from datetime import date, timedelta
from decimal import Decimal

from app.extensions import db
from app.models import (
    Brand,
    MediaOwner,
    Channel,
    Location,
    AudienceSegment,
    Campaign,
    campaign_channels,
    campaign_locations,
    campaign_audiences,
)


def seed_campaigns():
    """Seed realistic AdTech campaigns and campaign relationships."""

    brands = Brand.query.all()
    media_owners = MediaOwner.query.all()
    channels = Channel.query.all()
    locations = Location.query.all()
    audiences = AudienceSegment.query.all()

    if not brands:
        raise RuntimeError("Brands must be seeded before campaigns.")
    if not channels:
        raise RuntimeError("Channels must be seeded before campaigns.")
    if not locations:
        raise RuntimeError("Locations must be seeded before campaigns.")
    if not audiences:
        raise RuntimeError("Audiences must be seeded before campaigns.")

    objectives = [
        "Brand Awareness",
        "Lead Generation",
        "Conversions",
        "App Installs",
        "Product Launch",
        "Customer Acquisition",
        "Retargeting",
        "Sales Growth",
    ]

    statuses = [
        "COMPLETED",
        "COMPLETED",
        "COMPLETED",
        "ACTIVE",
        "ACTIVE",
        "PAUSED",
        "SCHEDULED",
    ]

    campaign_names = [
        "India Growth Campaign",
        "Summer Brand Activation",
        "Digital Reach 360",
        "Urban Consumer Connect",
        "Next Generation Campaign",
        "Premium Audience Drive",
        "Smart Mobility Campaign",
        "Festival Advertising Push",
        "Performance Max Initiative",
        "Connected Audience Campaign",
        "National Awareness Drive",
        "Customer Acquisition 360",
        "Digital First Campaign",
        "Urban Lifestyle Campaign",
        "Market Expansion Program",
    ]

    created = 0

    for i in range(30):
        brand = brands[i % len(brands)]
        media_owner = media_owners[i % len(media_owners)] if media_owners else None

        campaign_code = f"CAM{1001 + i}"

        existing = Campaign.query.filter_by(
            campaign_code=campaign_code
        ).first()

        if existing:
            continue

        start_date = date(2025, 1, 1) + timedelta(days=i * 10)
        end_date = start_date + timedelta(days=45 + (i % 4) * 15)

        budget = Decimal(
            250000 + (i * 75000)
        )

        campaign = Campaign(
            brand_id=brand.brand_id,
            media_owner_id=media_owner.media_owner_id if media_owner else None,
            campaign_name=campaign_names[i % len(campaign_names)],
            campaign_code=campaign_code,
            objective=objectives[i % len(objectives)],
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            status=statuses[i % len(statuses)],
        )

        db.session.add(campaign)
        db.session.flush()

        # Campaign ↔ Channels
        selected_channels = channels[i % len(channels):]
        selected_channels = selected_channels[:3]

        for j, channel in enumerate(selected_channels):
            db.session.execute(
                campaign_channels.insert().values(
                    campaign_id=campaign.campaign_id,
                    channel_id=channel.channel_id,
                    allocated_budget=budget
                    * Decimal(str(0.25 + (j * 0.10))),
                )
            )

        # Campaign ↔ Locations
        selected_locations = locations[i % len(locations):]
        selected_locations = selected_locations[:4]

        for location in selected_locations:
            db.session.execute(
                campaign_locations.insert().values(
                    campaign_id=campaign.campaign_id,
                    location_id=location.location_id,
                )
            )

        # Campaign ↔ Audiences
        selected_audiences = audiences[i % len(audiences):]
        selected_audiences = selected_audiences[:3]

        for audience in selected_audiences:
            db.session.execute(
                campaign_audiences.insert().values(
                    campaign_id=campaign.campaign_id,
                    audience_segment_id=audience.audience_segment_id,
                )
            )

        created += 1

    db.session.commit()

    return created
