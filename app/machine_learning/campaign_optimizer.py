from app.services.analytics_service import AnalyticsService


class CampaignOptimizer:
    """
    AI-inspired campaign optimization engine.

    Evaluates campaign performance using:
    - ROAS
    - CTR
    - CPA
    - Conversion volume
    - Overall efficiency

    Produces:
    - Performance score out of 100
    - Campaign health
    - Budget recommendation
    - Recommended budget change
    - Explainable recommendation reason
    """

    @staticmethod
    def calculate_score(roas, ctr, cpa, conversions):
        """
        Calculate a granular campaign performance score out of 100.
        """

        score = 0

        # -------------------------------------------------
        # 1. ROAS — 40 points
        # -------------------------------------------------
        if roas >= 100:
            score += 40
        elif roas >= 90:
            score += 37
        elif roas >= 80:
            score += 34
        elif roas >= 70:
            score += 30
        elif roas >= 50:
            score += 25
        elif roas >= 30:
            score += 18
        elif roas >= 15:
            score += 10
        else:
            score += 5

        # -------------------------------------------------
        # 2. CTR — 20 points
        # -------------------------------------------------
        if ctr >= 6:
            score += 20
        elif ctr >= 5:
            score += 18
        elif ctr >= 4:
            score += 16
        elif ctr >= 3:
            score += 14
        elif ctr >= 2:
            score += 10
        elif ctr >= 1:
            score += 6
        else:
            score += 2

        # -------------------------------------------------
        # 3. CPA — 20 points
        # -------------------------------------------------
        if cpa <= 20:
            score += 20
        elif cpa <= 30:
            score += 18
        elif cpa <= 40:
            score += 16
        elif cpa <= 50:
            score += 14
        elif cpa <= 75:
            score += 10
        elif cpa <= 100:
            score += 6
        else:
            score += 2

        # -------------------------------------------------
        # 4. Conversion volume — 10 points
        # -------------------------------------------------
        if conversions >= 500000:
            score += 10
        elif conversions >= 300000:
            score += 9
        elif conversions >= 200000:
            score += 8
        elif conversions >= 100000:
            score += 6
        elif conversions >= 50000:
            score += 4
        elif conversions > 0:
            score += 2

        # -------------------------------------------------
        # 5. Efficiency bonus — 10 points
        # -------------------------------------------------
        if roas >= 80 and cpa <= 40 and ctr >= 3:
            score += 10
        elif roas >= 50 and cpa <= 50 and ctr >= 2:
            score += 8
        elif roas >= 30 and cpa <= 75:
            score += 6
        elif roas >= 15:
            score += 4
        else:
            score += 1

        return min(score, 100)

    @staticmethod
    def generate_recommendation(score):
        """
        Convert performance score into an optimization recommendation.
        """

        if score >= 90:
            return (
                "EXCELLENT",
                "INCREASE_BUDGET",
                "+20%",
            )

        if score >= 80:
            return (
                "VERY_GOOD",
                "INCREASE_BUDGET",
                "+10%",
            )

        if score >= 70:
            return (
                "GOOD",
                "OPTIMIZE_CAMPAIGN",
                "+5%",
            )

        if score >= 55:
            return (
                "AVERAGE",
                "MAINTAIN_BUDGET",
                "0%",
            )

        if score >= 40:
            return (
                "NEEDS_ATTENTION",
                "MONITOR_CAMPAIGN",
                "-10%",
            )

        return (
            "POOR",
            "REDUCE_BUDGET",
            "-20%",
        )

    @staticmethod
    def generate_reason(roas, ctr, cpa, conversions, recommendation):
        """
        Generate an explainable reason for the recommendation.
        """

        reasons = []

        # ROAS
        if roas >= 90:
            reasons.append("Exceptional ROAS")
        elif roas >= 70:
            reasons.append("Strong ROAS")
        elif roas >= 50:
            reasons.append("Healthy ROAS")
        elif roas >= 30:
            reasons.append("Moderate ROAS")
        else:
            reasons.append("Low ROAS")

        # CTR
        if ctr >= 5:
            reasons.append("Excellent audience engagement")
        elif ctr >= 3:
            reasons.append("Good audience engagement")
        elif ctr >= 1.5:
            reasons.append("Average audience engagement")
        else:
            reasons.append("Low audience engagement")

        # CPA
        if cpa <= 30:
            reasons.append("Very efficient acquisition cost")
        elif cpa <= 50:
            reasons.append("Efficient acquisition cost")
        elif cpa <= 100:
            reasons.append("Acceptable acquisition cost")
        else:
            reasons.append("High acquisition cost")

        # Conversions
        if conversions >= 300000:
            reasons.append("High conversion volume")
        elif conversions >= 100000:
            reasons.append("Healthy conversion volume")
        elif conversions > 0:
            reasons.append("Limited conversion volume")
        else:
            reasons.append("No conversions recorded")

        # Recommendation context
        if recommendation == "INCREASE_BUDGET":
            reasons.append("Campaign shows strong scaling potential")

        elif recommendation == "OPTIMIZE_CAMPAIGN":
            reasons.append("Campaign has optimization opportunities")

        elif recommendation == "MAINTAIN_BUDGET":
            reasons.append("Current budget appears appropriate")

        elif recommendation == "MONITOR_CAMPAIGN":
            reasons.append("Campaign requires closer monitoring")

        elif recommendation == "REDUCE_BUDGET":
            reasons.append("Campaign efficiency is below target")

        return "; ".join(reasons)

    @staticmethod
    def analyze_campaign(campaign):
        """
        Analyze a single campaign.
        """

        spend = float(campaign.get("spend", 0) or 0)
        revenue = float(campaign.get("revenue", 0) or 0)
        impressions = int(campaign.get("impressions", 0) or 0)
        clicks = int(campaign.get("clicks", 0) or 0)
        conversions = int(campaign.get("conversions", 0) or 0)

        # -------------------------------------------------
        # KPI calculations
        # -------------------------------------------------

        ctr = (
            (clicks / impressions) * 100
            if impressions > 0
            else 0
        )

        cpc = (
            spend / clicks
            if clicks > 0
            else 0
        )

        cpa = (
            spend / conversions
            if conversions > 0
            else 0
        )

        roas = (
            revenue / spend
            if spend > 0
            else 0
        )

        # -------------------------------------------------
        # Performance score
        # -------------------------------------------------

        score = CampaignOptimizer.calculate_score(
            roas=roas,
            ctr=ctr,
            cpa=cpa,
            conversions=conversions,
        )

        # -------------------------------------------------
        # Recommendation
        # -------------------------------------------------

        health, recommendation, budget_change = (
            CampaignOptimizer.generate_recommendation(score)
        )

        # -------------------------------------------------
        # Explainable reason
        # -------------------------------------------------

        reason = CampaignOptimizer.generate_reason(
            roas=roas,
            ctr=ctr,
            cpa=cpa,
            conversions=conversions,
            recommendation=recommendation,
        )

        return {
            "campaign_id": campaign.get("campaign_id"),
            "campaign_name": campaign.get("campaign_name"),
            "health": health,
            "performance_score": score,
            "recommendation": recommendation,
            "recommended_budget_change": budget_change,
            "reason": reason,
            "metrics": {
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": round(spend, 2),
                "revenue": round(revenue, 2),
                "ctr": round(ctr, 2),
                "cpc": round(cpc, 2),
                "cpa": round(cpa, 2),
                "roas": round(roas, 2),
            },
        }

    @staticmethod
    def optimize_all_campaigns():
        """
        Analyze all campaigns and generate recommendations.
        """

        campaigns = AnalyticsService.get_campaign_performance()

        recommendations = [
            CampaignOptimizer.analyze_campaign(campaign)
            for campaign in campaigns
        ]

        # Highest-performing campaigns first
        recommendations.sort(
            key=lambda item: item["performance_score"],
            reverse=True,
        )

        return recommendations