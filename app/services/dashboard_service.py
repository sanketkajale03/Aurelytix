from sqlalchemy import func

from app.extensions import db
from app.models import (
    Agency,
    Advertiser,
    Brand,
    Campaign,
    CampaignPerformance,
)


class DashboardService:

    @staticmethod
    def get_dashboard():

        total_agencies = db.session.query(func.count(Agency.agency_id)).scalar()

        total_advertisers = db.session.query(
            func.count(Advertiser.advertiser_id)
        ).scalar()

        total_brands = db.session.query(
            func.count(Brand.brand_id)
        ).scalar()

        total_campaigns = db.session.query(
            func.count(Campaign.campaign_id)
        ).scalar()

        active_campaigns = db.session.query(
            func.count(Campaign.campaign_id)
        ).filter(
            Campaign.status == "ACTIVE"
        ).scalar()

        total_spend = db.session.query(
            func.coalesce(func.sum(CampaignPerformance.spend), 0)
        ).scalar()

        total_revenue = db.session.query(
            func.coalesce(func.sum(CampaignPerformance.revenue), 0)
        ).scalar()

        total_impressions = db.session.query(
            func.coalesce(func.sum(CampaignPerformance.impressions), 0)
        ).scalar()

        total_clicks = db.session.query(
            func.coalesce(func.sum(CampaignPerformance.clicks), 0)
        ).scalar()

        ctr = (
            (total_clicks / total_impressions) * 100
            if total_impressions
            else 0
        )

        cpc = (
            total_spend / total_clicks
            if total_clicks
            else 0
        )

        roas = (
            total_revenue / total_spend
            if total_spend
            else 0
        )

        return {
            "agencies": total_agencies,
            "advertisers": total_advertisers,
            "brands": total_brands,
            "campaigns": total_campaigns,
            "active_campaigns": active_campaigns,
            "spend": float(total_spend),
            "revenue": float(total_revenue),
            "impressions": total_impressions,
            "clicks": total_clicks,
            "ctr": round(ctr, 2),
            "cpc": round(cpc, 2),
            "roas": round(roas, 2),
        }