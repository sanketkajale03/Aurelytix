from app.extensions import db
from app.models import Campaign


class CampaignService:
    """Business logic for campaign management."""

    @staticmethod
    def get_all():
        """Return all campaigns."""
        campaigns = Campaign.query.order_by(
            Campaign.created_at.desc()
        ).all()

        return [
            {
                "campaign_id": campaign.campaign_id,
                "campaign_code": campaign.campaign_code,
                "campaign_name": campaign.campaign_name,
                "brand_id": campaign.brand_id,
                "media_owner_id": campaign.media_owner_id,
                "objective": campaign.objective,
                "start_date": campaign.start_date.isoformat(),
                "end_date": campaign.end_date.isoformat(),
                "budget": float(campaign.budget),
                "status": campaign.status,
            }
            for campaign in campaigns
        ]

    @staticmethod
    def get_by_id(campaign_id):
        """Return a single campaign."""
        campaign = db.session.get(Campaign, campaign_id)

        if campaign is None:
            return None

        return {
            "campaign_id": campaign.campaign_id,
            "campaign_code": campaign.campaign_code,
            "campaign_name": campaign.campaign_name,
            "brand_id": campaign.brand_id,
            "media_owner_id": campaign.media_owner_id,
            "objective": campaign.objective,
            "start_date": campaign.start_date.isoformat(),
            "end_date": campaign.end_date.isoformat(),
            "budget": float(campaign.budget),
            "status": campaign.status,
        }

    @staticmethod
    def create(data):
        """Create a new campaign."""

        campaign = Campaign(
            brand_id=data["brand_id"],
            media_owner_id=data.get("media_owner_id"),
            campaign_name=data["campaign_name"],
            campaign_code=data["campaign_code"],
            objective=data.get("objective"),
            start_date=data["start_date"],
            end_date=data["end_date"],
            budget=data.get("budget", 0),
            status=data.get("status", "DRAFT"),
        )

        db.session.add(campaign)
        db.session.commit()

        return CampaignService.get_by_id(campaign.campaign_id)

    @staticmethod
    def update(campaign_id, data):
        """Update an existing campaign."""

        campaign = db.session.get(Campaign, campaign_id)

        if campaign is None:
            return None

        allowed_fields = [
            "brand_id",
            "media_owner_id",
            "campaign_name",
            "campaign_code",
            "objective",
            "start_date",
            "end_date",
            "budget",
            "status",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(campaign, field, data[field])

        db.session.commit()

        return CampaignService.get_by_id(campaign_id)

    @staticmethod
    def delete(campaign_id):
        """Delete a campaign."""

        campaign = db.session.get(Campaign, campaign_id)

        if campaign is None:
            return False

        db.session.delete(campaign)
        db.session.commit()

        return True