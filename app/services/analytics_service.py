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
    def safe_divide(numerator, denominator):
        if denominator in (None, 0):
            return 0

        return numerator / denominator

    @staticmethod
    def get_kpis():
        result = db.session.query(
            func.coalesce(
                func.sum(CampaignPerformance.impressions), 0
            ).label("impressions"),

            func.coalesce(
                func.sum(CampaignPerformance.clicks), 0
            ).label("clicks"),

            func.coalesce(
                func.sum(CampaignPerformance.conversions), 0
            ).label("conversions"),

            func.coalesce(
                func.sum(CampaignPerformance.spend), 0
            ).label("spend"),

            func.coalesce(
                func.sum(CampaignPerformance.revenue), 0
            ).label("revenue"),
        ).first()

        impressions = int(result.impressions or 0)
        clicks = int(result.clicks or 0)
        conversions = int(result.conversions or 0)
        spend = float(result.spend or 0)
        revenue = float(result.revenue or 0)

        ctr = (
            AnalyticsService.safe_divide(clicks, impressions) * 100
        )

        cpc = AnalyticsService.safe_divide(
            spend,
            clicks
        )

        cpm = (
            AnalyticsService.safe_divide(spend, impressions) * 1000
        )

        conversion_rate = (
            AnalyticsService.safe_divide(conversions, clicks) * 100
        )

        cpa = AnalyticsService.safe_divide(
            spend,
            conversions
        )

        roas = AnalyticsService.safe_divide(
            revenue,
            spend
        )

        return {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "spend": round(spend, 2),
            "revenue": round(revenue, 2),
            "ctr": round(ctr, 2),
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
            "conversion_rate": round(
                conversion_rate,
                2
            ),
            "cpa": round(cpa, 2),
            "roas": round(roas, 2),
        }

    @staticmethod
    def get_channel_performance():
        rows = db.session.query(
            Channel.channel_id,
            Channel.channel_name,
            Channel.channel_type,

            func.coalesce(
                func.sum(
                    CampaignPerformance.impressions
                ),
                0
            ).label("impressions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.clicks
                ),
                0
            ).label("clicks"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.conversions
                ),
                0
            ).label("conversions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.spend
                ),
                0
            ).label("spend"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.revenue
                ),
                0
            ).label("revenue"),

        ).join(
            CampaignPerformance,
            CampaignPerformance.channel_id
            == Channel.channel_id
        ).group_by(
            Channel.channel_id,
            Channel.channel_name,
            Channel.channel_type,
        ).order_by(
            func.sum(
                CampaignPerformance.spend
            ).desc()
        ).all()

        data = []

        for row in rows:

            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            conversions = int(row.conversions or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            data.append({
                "channel_id": row.channel_id,
                "channel_name": row.channel_name,
                "channel_type": row.channel_type,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": round(spend, 2),
                "revenue": round(revenue, 2),
                "ctr": round(
                    AnalyticsService.safe_divide(
                        clicks,
                        impressions
                    ) * 100,
                    2
                ),
                "cpc": round(
                    AnalyticsService.safe_divide(
                        spend,
                        clicks
                    ),
                    2
                ),
                "roas": round(
                    AnalyticsService.safe_divide(
                        revenue,
                        spend
                    ),
                    2
                ),
            })

        return data

    @staticmethod
    def get_campaign_performance():
        rows = db.session.query(
            Campaign.campaign_id,
            Campaign.campaign_name,
            Campaign.campaign_code,
            Campaign.status,

            func.coalesce(
                func.sum(
                    CampaignPerformance.impressions
                ),
                0
            ).label("impressions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.clicks
                ),
                0
            ).label("clicks"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.conversions
                ),
                0
            ).label("conversions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.spend
                ),
                0
            ).label("spend"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.revenue
                ),
                0
            ).label("revenue"),

        ).outerjoin(
            CampaignPerformance,
            CampaignPerformance.campaign_id
            == Campaign.campaign_id
        ).group_by(
            Campaign.campaign_id,
            Campaign.campaign_name,
            Campaign.campaign_code,
            Campaign.status,
        ).order_by(
            func.sum(
                CampaignPerformance.spend
            ).desc()
        ).all()

        data = []

        for row in rows:

            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            conversions = int(row.conversions or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            data.append({
                "campaign_id": row.campaign_id,
                "campaign_name": row.campaign_name,
                "campaign_code": row.campaign_code,
                "status": row.status,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": round(spend, 2),
                "revenue": round(revenue, 2),
                "ctr": round(
                    AnalyticsService.safe_divide(
                        clicks,
                        impressions
                    ) * 100,
                    2
                ),
                "cpc": round(
                    AnalyticsService.safe_divide(
                        spend,
                        clicks
                    ),
                    2
                ),
                "cpa": round(
                    AnalyticsService.safe_divide(
                        spend,
                        conversions
                    ),
                    2
                ),
                "roas": round(
                    AnalyticsService.safe_divide(
                        revenue,
                        spend
                    ),
                    2
                ),
            })

        return data

    @staticmethod
    def get_location_performance():
        rows = db.session.query(
            Location.location_id,
            Location.country,
            Location.state,
            Location.city,

            func.coalesce(
                func.sum(
                    CampaignPerformance.impressions
                ),
                0
            ).label("impressions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.clicks
                ),
                0
            ).label("clicks"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.conversions
                ),
                0
            ).label("conversions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.spend
                ),
                0
            ).label("spend"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.revenue
                ),
                0
            ).label("revenue"),

        ).join(
            CampaignPerformance,
            CampaignPerformance.location_id
            == Location.location_id
        ).group_by(
            Location.location_id,
            Location.country,
            Location.state,
            Location.city,
        ).order_by(
            func.sum(
                CampaignPerformance.spend
            ).desc()
        ).all()

        data = []

        for row in rows:

            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            conversions = int(row.conversions or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            data.append({
                "location_id": row.location_id,
                "country": row.country,
                "state": row.state,
                "city": row.city,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": round(spend, 2),
                "revenue": round(revenue, 2),
                "ctr": round(
                    AnalyticsService.safe_divide(
                        clicks,
                        impressions
                    ) * 100,
                    2
                ),
                "roas": round(
                    AnalyticsService.safe_divide(
                        revenue,
                        spend
                    ),
                    2
                ),
            })

        return data

    @staticmethod
    def get_daily_trends():
        rows = db.session.query(
            CampaignPerformance.performance_date,

            func.coalesce(
                func.sum(
                    CampaignPerformance.impressions
                ),
                0
            ).label("impressions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.clicks
                ),
                0
            ).label("clicks"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.conversions
                ),
                0
            ).label("conversions"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.spend
                ),
                0
            ).label("spend"),

            func.coalesce(
                func.sum(
                    CampaignPerformance.revenue
                ),
                0
            ).label("revenue"),

        ).group_by(
            CampaignPerformance.performance_date
        ).order_by(
            CampaignPerformance.performance_date.asc()
        ).all()

        data = []

        for row in rows:

            impressions = int(row.impressions or 0)
            clicks = int(row.clicks or 0)
            conversions = int(row.conversions or 0)
            spend = float(row.spend or 0)
            revenue = float(row.revenue or 0)

            data.append({
                "date": row.performance_date.isoformat(),
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": round(spend, 2),
                "revenue": round(revenue, 2),
                "ctr": round(
                    AnalyticsService.safe_divide(
                        clicks,
                        impressions
                    ) * 100,
                    2
                ),
                "roas": round(
                    AnalyticsService.safe_divide(
                        revenue,
                        spend
                    ),
                    2
                ),
            })

        return data