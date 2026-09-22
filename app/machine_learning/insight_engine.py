from app.machine_learning.campaign_optimizer import CampaignOptimizer
from app.machine_learning.campaign_forecaster import CampaignForecaster
from app.machine_learning.anomaly_detector import AnomalyDetector
from app.services.analytics_service import AnalyticsService


class InsightEngine:
    """
    Generates business-level insights by combining
    optimization, forecasting, and anomaly detection.
    """

    @staticmethod
    def generate_insights(campaign_id):

        campaigns = AnalyticsService.get_campaign_performance()

        campaign = next(
            (
                item for item in campaigns
                if int(item.get("campaign_id", 0)) == int(campaign_id)
            ),
            None,
        )

        if campaign is None:
            return {
                "campaign_id": campaign_id,
                "error": "Campaign not found."
            }

        optimization = CampaignOptimizer.analyze_campaign(campaign)

        forecast = CampaignForecaster.forecast_campaign(
            campaign_id,
            days=7
        )

        anomalies = AnomalyDetector.detect_campaign_anomalies(
            campaign_id
        )

        if "error" in forecast:
            return {
                "campaign_id": campaign_id,
                "error": forecast["error"]
            }

        if "error" in anomalies:
            return {
                "campaign_id": campaign_id,
                "error": anomalies["error"]
            }

        metrics = optimization.get("metrics", {})

        roas = float(metrics.get("roas", 0) or 0)
        ctr = float(metrics.get("ctr", 0) or 0)
        cpa = float(metrics.get("cpa", 0) or 0)

        performance_score = float(
            optimization.get("performance_score", 0) or 0
        )

        anomaly_count = int(
            anomalies.get("anomaly_count", 0) or 0
        )

        forecast_data = forecast.get("forecast", [])

        average_forecast_roas = (
            sum(
                float(item.get("roas", 0) or 0)
                for item in forecast_data
            ) / len(forecast_data)
            if forecast_data
            else 0
        )

        insights = []
        priorities = []

        if performance_score >= 80:
            insights.append(
                "Campaign performance is strong and suitable for controlled budget scaling."
            )
            priorities.append("HIGH")
        elif performance_score >= 70:
            insights.append(
                "Campaign performance is healthy but optimization opportunities remain."
            )
            priorities.append("MEDIUM")
        elif performance_score >= 55:
            insights.append(
                "Campaign performance is stable and should be monitored closely."
            )
            priorities.append("MEDIUM")
        else:
            insights.append(
                "Campaign performance requires optimization before additional budget is allocated."
            )
            priorities.append("HIGH")

        if roas >= 80:
            insights.append(
                f"ROAS is strong at {roas:.2f}, indicating efficient revenue generation."
            )
        elif roas < 50:
            insights.append(
                f"ROAS is relatively low at {roas:.2f}; budget efficiency should be improved."
            )

        if ctr >= 3:
            insights.append(
                f"CTR is healthy at {ctr:.2f}%, indicating strong audience engagement."
            )
        elif ctr < 2:
            insights.append(
                f"CTR is low at {ctr:.2f}%; creative or audience targeting should be reviewed."
            )
            priorities.append("HIGH")

        if cpa > 100:
            insights.append(
                f"CPA is high at {cpa:.2f}; conversion acquisition costs should be reduced."
            )
            priorities.append("HIGH")
        elif cpa > 0:
            insights.append(
                f"CPA is {cpa:.2f}, indicating the current conversion acquisition efficiency."
            )

        if average_forecast_roas > roas:
            insights.append(
                "The 7-day forecast indicates improving future ROAS."
            )
        elif average_forecast_roas < roas:
            insights.append(
                "The 7-day forecast indicates potential ROAS deterioration."
            )
            priorities.append("HIGH")

        if anomaly_count > 0:
            insights.append(
                f"{anomaly_count} statistical performance anomalies were detected and should be investigated."
            )
            priorities.append("HIGH")
        else:
            insights.append(
                "No significant statistical anomalies were detected."
            )

        if "HIGH" in priorities:
            overall_priority = "HIGH"
        elif "MEDIUM" in priorities:
            overall_priority = "MEDIUM"
        else:
            overall_priority = "LOW"

        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign.get("campaign_name"),
            "performance_score": round(performance_score, 2),
            "current_metrics": {
                "roas": round(roas, 2),
                "ctr": round(ctr, 2),
                "cpa": round(cpa, 2),
            },
            "forecast": {
                "forecast_days": 7,
                "average_forecast_roas": round(
                    average_forecast_roas,
                    2
                ),
            },
            "anomaly_summary": {
                "anomaly_count": anomaly_count,
                "status": anomalies.get("status"),
            },
            "overall_priority": overall_priority,
            "insights": insights,
        }
