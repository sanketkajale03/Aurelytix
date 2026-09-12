from app.extensions import db
from sqlalchemy import text


class GeographicOptimizer:
    """
    AI-driven geographic campaign optimization engine.

    Evaluates campaign performance by:
    - Country
    - State
    - City
    - Impressions
    - Clicks
    - Conversions
    - Spend
    - Revenue
    - CTR
    - Conversion Rate
    - CPA
    - ROAS
    """

    @staticmethod
    def analyze_locations():
        query = text("""
            SELECT
                l.location_id,
                l.country,
                l.state,
                l.city,
                l.latitude,
                l.longitude,
                COALESCE(SUM(cp.impressions), 0) AS impressions,
                COALESCE(SUM(cp.clicks), 0) AS clicks,
                COALESCE(SUM(cp.conversions), 0) AS conversions,
                COALESCE(SUM(cp.spend), 0) AS spend,
                COALESCE(SUM(cp.revenue), 0) AS revenue
            FROM locations l
            LEFT JOIN campaign_performance cp
                ON l.location_id = cp.location_id
            GROUP BY
                l.location_id,
                l.country,
                l.state,
                l.city,
                l.latitude,
                l.longitude
            ORDER BY revenue DESC
        """)

        rows = db.session.execute(query).mappings().all()

        results = []

        for row in rows:
            impressions = float(row["impressions"] or 0)
            clicks = float(row["clicks"] or 0)
            conversions = float(row["conversions"] or 0)
            spend = float(row["spend"] or 0)
            revenue = float(row["revenue"] or 0)

            ctr = (
                clicks / impressions * 100
                if impressions
                else 0
            )

            conversion_rate = (
                conversions / clicks * 100
                if clicks
                else 0
            )

            cpa = (
                spend / conversions
                if conversions
                else 0
            )

            roas = (
                revenue / spend
                if spend
                else 0
            )

            score = 0

            # ROAS — 40 points
            if roas >= 100:
                score += 40
            elif roas >= 80:
                score += 35
            elif roas >= 60:
                score += 30
            elif roas >= 40:
                score += 20
            elif roas >= 20:
                score += 10

            # CTR — 25 points
            if ctr >= 5:
                score += 25
            elif ctr >= 4:
                score += 20
            elif ctr >= 3:
                score += 15
            elif ctr >= 2:
                score += 10
            else:
                score += 5

            # Conversion Rate — 20 points
            if conversion_rate >= 10:
                score += 20
            elif conversion_rate >= 7:
                score += 16
            elif conversion_rate >= 5:
                score += 12
            elif conversion_rate >= 3:
                score += 8
            else:
                score += 4

            # CPA — 15 points
            if cpa <= 25:
                score += 15
            elif cpa <= 40:
                score += 12
            elif cpa <= 60:
                score += 9
            elif cpa <= 100:
                score += 5

            if score >= 85:
                location_rating = "HIGH_VALUE"
                action = "INCREASE_BUDGET"
                priority = "HIGH"

            elif score >= 70:
                location_rating = "STRONG"
                action = "EXPAND_REGION"
                priority = "MEDIUM"

            elif score >= 55:
                location_rating = "AVERAGE"
                action = "MAINTAIN_BUDGET"
                priority = "MEDIUM"

            elif ctr < 2:
                location_rating = "LOW_ENGAGEMENT"
                action = "IMPROVE_TARGETING"
                priority = "HIGH"

            elif cpa > 100:
                location_rating = "HIGH_ACQUISITION_COST"
                action = "REDUCE_SPEND"
                priority = "HIGH"

            else:
                location_rating = "NEEDS_ATTENTION"
                action = "MONITOR_LOCATION"
                priority = "LOW"

            results.append({
                "location_id": row["location_id"],
                "location": {
                    "country": row["country"],
                    "state": row["state"],
                    "city": row["city"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                },
                "metrics": {
                    "impressions": int(impressions),
                    "clicks": int(clicks),
                    "conversions": int(conversions),
                    "spend": round(spend, 2),
                    "revenue": round(revenue, 2),
                    "ctr": round(ctr, 2),
                    "conversion_rate": round(conversion_rate, 2),
                    "cpa": round(cpa, 2),
                    "roas": round(roas, 2),
                },
                "performance_score": score,
                "location_rating": location_rating,
                "recommendation": {
                    "action": action,
                    "priority": priority,
                },
            })

        return results