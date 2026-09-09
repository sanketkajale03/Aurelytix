from app import create_app
from app.extensions import db

from app.seeds.agency_seed import seed_agencies
from app.seeds.advertiser_seed import seed_advertisers
from app.seeds.brand_seed import seed_brands
from app.seeds.media_owner_seed import seed_media_owners
from app.seeds.channel_seed import seed_channels
from app.seeds.location_seed import seed_locations
from app.seeds.audience_seed import seed_audiences
from app.seeds.campaign_seed import seed_campaigns
from app.seeds.performance_seed import seed_performance_records


def run_seed():
    """Execute all database seed operations."""

    print("\n========================================")
    print("       AURELYTIX DATABASE SEED")
    print("========================================\n")

    print("1. Agencies...")
    print(f"   Created: {seed_agencies()}")

    print("2. Advertisers...")
    print(f"   Created: {seed_advertisers()}")

    print("3. Brands...")
    print(f"   Created: {seed_brands()}")

    print("4. Media Owners...")
    print(f"   Created: {seed_media_owners()}")

    print("5. Channels...")
    print(f"   Created: {seed_channels()}")

    print("6. Locations...")
    print(f"   Created: {seed_locations()}")

    print("7. Audience Segments...")
    print(f"   Created: {seed_audiences()}")

    print("8. Campaigns...")
    print(f"   Created: {seed_campaigns()}")

    print("9. Performance Records...")
    created = seed_performance_records(
        records_per_campaign=1800
    )

    print(f"   Created: {created:,}")

    print("\n========================================")
    print("       SEEDING COMPLETED")
    print("========================================\n")


if __name__ == "__main__":
    application = create_app()

    with application.app_context():
        run_seed()
