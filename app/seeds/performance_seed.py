from datetime import date, timedelta
from decimal import Decimal
import random

from app.extensions import db
from app.models import Campaign, Channel, Location, CampaignPerformance


def seed_performance_records(records_per_campaign=1800):
    """Generate realistic campaign-performance data."""

    campaigns = Campaign.query.all()
    channels = Channel.query.all()
    locations = Location.query.all()

    if not campaigns:
        raise RuntimeError("Campaigns must be seeded before performance data.")

    if not channels:
        raise RuntimeError("Channels must be seeded before performance data.")

    if not locations:
        raise RuntimeError("Locations must be seeded before performance data.")

    random.seed(42)

    total_created = 0
    batch = []

    for campaign_index, campaign in enumerate(campaigns):

        existing_count = CampaignPerformance.query.filter_by(
            campaign_id=campaign.campaign_id
        ).count()

        if existing_count > 0:
            continue

        campaign_channels = channels[
            campaign_index % len(channels):
        ]

        if not campaign_channels:
            campaign_channels = channels

        campaign_locations = locations[
            campaign_index % len(locations):
        ]

        if not campaign_locations:
            campaign_locations = locations

        start_date = campaign.start_date
        end_date = campaign.end_date

        campaign_days = (end_date - start_date).days + 1

        for record_index in range(records_per_campaign):

            performance_date = start_date + timedelta(
                days=record_index % campaign_days
            )

            channel = campaign_channels[
                record_index % len(campaign_channels)
            ]

            location = campaign_locations[
                record_index % len(campaign_locations)
            ]

            impressions = random.randint(
                5000,
                150000
            )

            ctr = random.uniform(
                0.008,
                0.065
            )

            clicks = int(
                impressions * ctr
            )

            conversion_rate = random.uniform(
                0.015,
                0.12
            )

            conversions = int(
                clicks * conversion_rate
            )

            spend = Decimal(
                str(
                    round(
                        random.uniform(500, 15000),
                        2
                    )
                )
            )

            revenue_per_conversion = random.uniform(
                1200,
                6500
            )

            revenue = Decimal(
                str(
                    round(
                        conversions * revenue_per_conversion,
                        2
                    )
                )
            )

            batch.append(
                CampaignPerformance(
                    campaign_id=campaign.campaign_id,
                    channel_id=channel.channel_id,
                    location_id=location.location_id,
                    performance_date=performance_date,
                    impressions=impressions,
                    clicks=clicks,
                    conversions=conversions,
                    spend=spend,
                    revenue=revenue,
                )
            )

            total_created += 1

            if len(batch) >= 1000:
                db.session.bulk_save_objects(batch)
                db.session.commit()
                batch.clear()

                print(
                    f"Inserted {total_created:,} performance records..."
                )

    if batch:
        db.session.bulk_save_objects(batch)
        db.session.commit()

    return total_created
