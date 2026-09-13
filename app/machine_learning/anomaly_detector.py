from app.extensions import db
from sqlalchemy import text


class AnomalyDetector:

    @staticmethod
    def detect_campaign_anomalies(campaign_id):

        query = text("""
            SELECT
                DATE(performance_date) AS performance_date,
                SUM(impressions) AS impressions,
                SUM(clicks) AS clicks,
                SUM(conversions) AS conversions,
                SUM(spend) AS spend,
                SUM(revenue) AS revenue
            FROM campaign_performance
            WHERE campaign_id = :campaign_id
            GROUP BY DATE(performance_date)
            ORDER BY DATE(performance_date)
        """)

        rows = db.session.execute(
            query,
            {"campaign_id": campaign_id}
        ).mappings().all()

        if not rows:
            return {
                "campaign_id": campaign_id,
                "error": "Campaign not found or no performance data available."
            }

        daily_data = []

        for row in rows:
            impressions = float(row["impressions"] or 0)
            clicks = float(row["clicks"] or 0)
            conversions = float(row["conversions"] or 0)
            spend = float(row["spend"] or 0)
            revenue = float(row["revenue"] or 0)

            ctr = (
                clicks / impressions * 100
                if impressions else 0
            )

            cpa = (
                spend / conversions
                if conversions else 0
            )

            roas = (
                revenue / spend
                if spend else 0
            )

            daily_data.append({
                "date": row["performance_date"],
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": spend,
                "revenue": revenue,
                "ctr": ctr,
                "cpa": cpa,
                "roas": roas,
            })

        anomalies = []

        metric_names = {
            "ctr": "CTR",
            "cpa": "CPA",
            "roas": "ROAS",
            "spend": "Spend",
            "conversions": "Conversions",
        }

        for metric_name, display_name in metric_names.items():

            values = [
                item[metric_name]
                for item in daily_data
                if item[metric_name] > 0
            ]

            if len(values) < 5:
                continue

            mean_value = sum(values) / len(values)

            variance = sum(
                (value - mean_value) ** 2
                for value in values
            ) / len(values)

            std_dev = variance ** 0.5

            if std_dev == 0:
                continue

            upper_threshold = mean_value + (2 * std_dev)
            lower_threshold = max(
                0,
                mean_value - (2 * std_dev)
            )

            for item in daily_data:

                value = item[metric_name]

                if value > upper_threshold:
                    anomalies.append({
                        "date": str(item["date"]),
                        "metric": display_name,
                        "value": round(value, 2),
                        "expected_range": {
                            "lower": round(lower_threshold, 2),
                            "upper": round(upper_threshold, 2),
                        },
                        "type": "SPIKE",
                        "severity": "HIGH",
                    })

                elif value < lower_threshold:
                    anomalies.append({
                        "date": str(item["date"]),
                        "metric": display_name,
                        "value": round(value, 2),
                        "expected_range": {
                            "lower": round(lower_threshold, 2),
                            "upper": round(upper_threshold, 2),
                        },
                        "type": "DROP",
                        "severity": "HIGH",
                    })

        if anomalies:
            status = "ANOMALIES_DETECTED"
            recommendation = (
                "Investigate unusual campaign performance "
                "before making major budget changes."
            )
        else:
            status = "NORMAL"
            recommendation = (
                "Campaign performance is within the "
                "expected statistical range."
            )

        return {
            "campaign_id": campaign_id,
            "historical_records": len(daily_data),
            "status": status,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "recommendation": recommendation,
        }
