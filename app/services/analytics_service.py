from sqlalchemy import func

from app.extensions import db
from app.models import (
    Campaign,
    CampaignPerformance,
    Channel,
    Location,
)


class AnalyticsService:

    @staticmethod
    def get_channel_performance():
        rows = (
            db.session.query(
                Channel.channel_name,
                func.sum(CampaignPerformance.impressions).label("impressions"),
                func.sum(CampaignPerformance.clicks).label("clicks"),
                func.sum(CampaignPerformance.conversions).label("conversions"),
                func.sum(CampaignPerformance.spend).label("spend"),
                func.sum(CampaignPerformance.revenue).label("revenue"),
            )
            .join(
                CampaignPerformance,
                CampaignPerformance.channel_id == Channel.channel_id,
            )
            .group_by(Channel.channel_id, Channel.channel_name)
            .order_by(func.sum(CampaignPerformance.revenue).desc())
            .all()
        )

        result = []

        for row in rows:
            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            conversions = int(row.conversions or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            result.append(
                {
                    "channel": row.channel_name,
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "spend": round(spend, 2),
                    "revenue": round(revenue, 2),
                    "ctr": round(
                        (clicks / impressions) * 100, 2
                    )
                    if impressions
                    else 0,
                    "cpc": round(
                        spend / clicks, 2
                    )
                    if clicks
                    else 0,
                    "roas": round(
                        revenue / spend, 2
                    )
                    if spend
                    else 0,
                }
            )

        return result

    @staticmethod
    def get_campaign_performance():
        rows = (
            db.session.query(
                Campaign.campaign_name,
                Campaign.campaign_code,
                Campaign.status,
                func.sum(CampaignPerformance.impressions).label(
                    "impressions"
                ),
                func.sum(CampaignPerformance.clicks).label(
                    "clicks"
                ),
                func.sum(CampaignPerformance.conversions).label(
                    "conversions"
                ),
                func.sum(CampaignPerformance.spend).label(
                    "spend"
                ),
                func.sum(CampaignPerformance.revenue).label(
                    "revenue"
                ),
            )
            .join(
                CampaignPerformance,
                CampaignPerformance.campaign_id == Campaign.campaign_id,
            )
            .group_by(
                Campaign.campaign_id,
                Campaign.campaign_name,
                Campaign.campaign_code,
                Campaign.status,
            )
            .order_by(
                func.sum(CampaignPerformance.revenue).desc()
            )
            .all()
        )

        result = []

        for row in rows:
            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            conversions = int(row.conversions or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            result.append(
                {
                    "campaign_name": row.campaign_name,
                    "campaign_code": row.campaign_code,
                    "status": row.status,
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "spend": round(spend, 2),
                    "revenue": round(revenue, 2),
                    "ctr": round(
                        (clicks / impressions) * 100, 2
                    )
                    if impressions
                    else 0,
                    "roas": round(
                        revenue / spend, 2
                    )
                    if spend
                    else 0,
                }
            )

        return result

    @staticmethod
    def get_location_performance():
        rows = (
            db.session.query(
                Location.city,
                Location.state,
                func.sum(CampaignPerformance.impressions).label(
                    "impressions"
                ),
                func.sum(CampaignPerformance.clicks).label(
                    "clicks"
                ),
                func.sum(CampaignPerformance.spend).label(
                    "spend"
                ),
                func.sum(CampaignPerformance.revenue).label(
                    "revenue"
                ),
            )
            .join(
                CampaignPerformance,
                CampaignPerformance.location_id == Location.location_id,
            )
            .group_by(
                Location.location_id,
                Location.city,
                Location.state,
            )
            .order_by(
                func.sum(CampaignPerformance.revenue).desc()
            )
            .all()
        )

        result = []

        for row in rows:
            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            result.append(
                {
                    "city": row.city,
                    "state": row.state,
                    "impressions": impressions,
                    "clicks": clicks,
                    "spend": round(spend, 2),
                    "revenue": round(revenue, 2),
                    "ctr": round(
                        (clicks / impressions) * 100, 2
                    )
                    if impressions
                    else 0,
                    "roas": round(
                        revenue / spend, 2
                    )
                    if spend
                    else 0,
                }
            )

        return result

    @staticmethod
    def get_daily_trends():
        rows = (
            db.session.query(
                CampaignPerformance.performance_date,
                func.sum(CampaignPerformance.impressions).label(
                    "impressions"
                ),
                func.sum(CampaignPerformance.clicks).label(
                    "clicks"
                ),
                func.sum(CampaignPerformance.conversions).label(
                    "conversions"
                ),
                func.sum(CampaignPerformance.spend).label(
                    "spend"
                ),
                func.sum(CampaignPerformance.revenue).label(
                    "revenue"
                ),
            )
            .group_by(CampaignPerformance.performance_date)
            .order_by(CampaignPerformance.performance_date)
            .all()
        )

        result = []

        for row in rows:
            result.append(
                {
                    "date": row.performance_date.isoformat(),
                    "impressions": int(row.impressions or 0),
                    "clicks": int(row.clicks or 0),
                    "conversions": int(row.conversions or 0),
                    "spend": round(float(row.spend or 0), 2),
                    "revenue": round(float(row.revenue or 0), 2),
                }
            )

        return result
