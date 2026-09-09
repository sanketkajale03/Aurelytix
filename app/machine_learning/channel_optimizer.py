from app.services.analytics_service import AnalyticsService


class ChannelOptimizer:
    """
    Channel-level budget optimization engine.

    Evaluates advertising channels using:
    - ROAS
    - CTR
    - CPC
    - Conversion volume
    - Spend efficiency
    """

    @staticmethod
    def calculate_score(channel):
        roas = float(channel.get("roas", 0) or 0)
        ctr = float(channel.get("ctr", 0) or 0)
        cpc = float(channel.get("cpc", 0) or 0)
        conversions = int(channel.get("conversions", 0) or 0)

        score = 0

        # ROAS — 40 points
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

        # CTR — 25 points
        if ctr >= 6:
            score += 25
        elif ctr >= 5:
            score += 22
        elif ctr >= 4:
            score += 19
        elif ctr >= 3:
            score += 16
        elif ctr >= 2:
            score += 11
        elif ctr >= 1:
            score += 6
        else:
            score += 2

        # CPC — 20 points
        if cpc <= 1:
            score += 20
        elif cpc <= 2:
            score += 18
        elif cpc <= 3:
            score += 16
        elif cpc <= 5:
            score += 12
        elif cpc <= 10:
            score += 8
        else:
            score += 3

        # Conversion volume — 15 points
        if conversions >= 3000000:
            score += 15
        elif conversions >= 2000000:
            score += 13
        elif conversions >= 1000000:
            score += 11
        elif conversions >= 500000:
            score += 8
        elif conversions >= 100000:
            score += 5
        elif conversions > 0:
            score += 2

        return min(score, 100)

    @staticmethod
    def generate_recommendation(score):
        if score >= 90:
            return "INCREASE_ALLOCATION", "+20%"

        if score >= 80:
            return "INCREASE_ALLOCATION", "+10%"

        if score >= 70:
            return "OPTIMIZE_ALLOCATION", "+5%"

        if score >= 55:
            return "MAINTAIN_ALLOCATION", "0%"

        if score >= 40:
            return "MONITOR_CHANNEL", "-10%"

        return "REDUCE_ALLOCATION", "-20%"

    @staticmethod
    def generate_reason(channel, score, recommendation):
        roas = float(channel.get("roas", 0) or 0)
        ctr = float(channel.get("ctr", 0) or 0)
        cpc = float(channel.get("cpc", 0) or 0)

        reasons = []

        if roas >= 80:
            reasons.append("strong ROAS")
        elif roas >= 50:
            reasons.append("healthy ROAS")
        else:
            reasons.append("weak ROAS")

        if ctr >= 4:
            reasons.append("excellent engagement")
        elif ctr >= 3:
            reasons.append("good engagement")
        else:
            reasons.append("low engagement")

        if cpc <= 3:
            reasons.append("efficient CPC")
        elif cpc <= 5:
            reasons.append("acceptable CPC")
        else:
            reasons.append("high CPC")

        if recommendation == "INCREASE_ALLOCATION":
            reasons.append("channel has strong scaling potential")

        elif recommendation == "OPTIMIZE_ALLOCATION":
            reasons.append("channel has optimization potential")

        elif recommendation == "MAINTAIN_ALLOCATION":
            reasons.append("current allocation is appropriate")

        elif recommendation == "MONITOR_CHANNEL":
            reasons.append("channel requires monitoring")

        else:
            reasons.append("allocation should be reduced")

        return ", ".join(reasons).capitalize() + "."

    @staticmethod
    def analyze_channel(channel):
        score = ChannelOptimizer.calculate_score(channel)

        recommendation, allocation_change = (
            ChannelOptimizer.generate_recommendation(score)
        )

        reason = ChannelOptimizer.generate_reason(
            channel,
            score,
            recommendation,
        )

        return {
            "channel_id": channel.get("channel_id"),
            "channel_name": channel.get("channel_name"),
            "channel_type": channel.get("channel_type"),
            "performance_score": score,
            "recommendation": recommendation,
            "recommended_allocation_change": allocation_change,
            "reason": reason,
            "metrics": {
                "impressions": int(channel.get("impressions", 0) or 0),
                "clicks": int(channel.get("clicks", 0) or 0),
                "conversions": int(channel.get("conversions", 0) or 0),
                "spend": round(float(channel.get("spend", 0) or 0), 2),
                "revenue": round(float(channel.get("revenue", 0) or 0), 2),
                "ctr": round(float(channel.get("ctr", 0) or 0), 2),
                "cpc": round(float(channel.get("cpc", 0) or 0), 2),
                "roas": round(float(channel.get("roas", 0) or 0), 2),
            },
        }

    @staticmethod
    def optimize_all_channels():
        channels = AnalyticsService.get_channel_performance()

        recommendations = [
            ChannelOptimizer.analyze_channel(channel)
            for channel in channels
        ]

        recommendations.sort(
            key=lambda item: item["performance_score"],
            reverse=True,
        )

        return recommendations