from app.services.analytics_service import AnalyticsService
from app.machine_learning.campaign_forecaster import CampaignForecaster
from app.machine_learning.campaign_optimizer import CampaignOptimizer


class RecommendationEngine:

    @staticmethod
    def generate_recommendation(campaign_id):
        # Get campaign performance data
        campaigns = AnalyticsService.get_campaign_performance()

        campaign = next(
            (
                item
                for item in campaigns
                if int(item.get("campaign_id", 0)) == int(campaign_id)
            ),
            None,
        )

        if campaign is None:
            return {
                "campaign_id": campaign_id,
                "error": "Campaign not found."
            }

        # Analyze campaign performance
        optimization = CampaignOptimizer.analyze_campaign(
            campaign
        )

        # Generate forecast
        forecast = CampaignForecaster.forecast_campaign(
            campaign_id,
            days=7,
        )

        if "error" in forecast:
            return {
                "campaign_id": campaign_id,
                "error": forecast["error"],
            }

        metrics = optimization.get("metrics", {})

        roas = float(metrics.get("roas", 0) or 0)
        ctr = float(metrics.get("ctr", 0) or 0)
        cpa = float(metrics.get("cpa", 0) or 0)

        score = optimization.get(
            "performance_score",
            0,
        )

        forecast_data = forecast.get(
            "forecast",
            [],
        )

        average_forecast_roas = (
            sum(
                item["roas"]
                for item in forecast_data
            )
            / len(forecast_data)
            if forecast_data
            else 0
        )

        # Recommendation logic
        if score >= 80 and average_forecast_roas >= roas:
            action = "INCREASE_BUDGET"
            priority = "HIGH"

            explanation = (
                "Campaign performance is strong and "
                "forecasted performance remains positive. "
                "Increasing budget is recommended."
            )

        elif score >= 70:
            action = "OPTIMIZE_CAMPAIGN"
            priority = "MEDIUM"

            explanation = (
                "Campaign is performing well but has "
                "optimization opportunities before "
                "significant budget scaling."
            )

        elif score >= 55:
            action = "MAINTAIN_BUDGET"
            priority = "MEDIUM"

            explanation = (
                "Campaign performance is stable. "
                "Maintain the current budget while "
                "monitoring performance."
            )

        elif ctr < 2:
            action = "OPTIMIZE_TARGETING"
            priority = "HIGH"

            explanation = (
                "Low CTR indicates that audience targeting "
                "or creative engagement should be improved."
            )

        elif cpa > 100:
            action = "REDUCE_ACQUISITION_COST"
            priority = "HIGH"

            explanation = (
                "High CPA indicates inefficient conversion "
                "acquisition. Campaign efficiency should "
                "be improved."
            )

        else:
            action = "MONITOR_CAMPAIGN"
            priority = "LOW"

            explanation = (
                "Campaign requires continued monitoring "
                "before making major budget changes."
            )

        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign.get(
                "campaign_name"
            ),
            "performance_score": score,

            "current_metrics": {
                "roas": round(roas, 2),
                "ctr": round(ctr, 2),
                "cpa": round(cpa, 2),
            },

            "forecast": {
                "forecast_days": 7,
                "average_forecast_roas": round(
                    average_forecast_roas,
                    2,
                ),
            },

            "recommendation": {
                "action": action,
                "priority": priority,
                "explanation": explanation,
            },
        }