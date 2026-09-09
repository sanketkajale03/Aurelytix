from app.services.analytics_service import AnalyticsService


class BudgetAllocator:
    """
    AI-inspired budget allocation engine.

    Allocates a total advertising budget across channels
    based on performance scores and ROAS.
    """

    @staticmethod
    def calculate_channel_score(channel):
        roas = float(channel.get("roas", 0) or 0)
        ctr = float(channel.get("ctr", 0) or 0)
        cpc = float(channel.get("cpc", 0) or 0)

        score = 0

        # ROAS — 50 points
        if roas >= 100:
            score += 50
        elif roas >= 90:
            score += 45
        elif roas >= 80:
            score += 40
        elif roas >= 70:
            score += 35
        elif roas >= 50:
            score += 28
        elif roas >= 30:
            score += 20
        elif roas >= 15:
            score += 10
        else:
            score += 5

        # CTR — 25 points
        if ctr >= 5:
            score += 25
        elif ctr >= 4:
            score += 22
        elif ctr >= 3:
            score += 18
        elif ctr >= 2:
            score += 12
        elif ctr >= 1:
            score += 7
        else:
            score += 2

        # CPC efficiency — 25 points
        if cpc <= 1:
            score += 25
        elif cpc <= 2:
            score += 22
        elif cpc <= 3:
            score += 18
        elif cpc <= 5:
            score += 13
        elif cpc <= 10:
            score += 7
        else:
            score += 2

        return min(score, 100)

    @staticmethod
    def allocate_budget(total_budget):
        """
        Allocate the supplied budget across all channels.
        """

        total_budget = float(total_budget)

        channels = AnalyticsService.get_channel_performance()

        if not channels:
            return {
                "total_budget": total_budget,
                "allocated_budget": 0,
                "channels": [],
            }

        scored_channels = []

        for channel in channels:
            score = BudgetAllocator.calculate_channel_score(channel)

            scored_channels.append({
                "channel": channel,
                "score": score,
            })

        total_score = sum(
            item["score"]
            for item in scored_channels
        )

        allocations = []

        for item in scored_channels:
            channel = item["channel"]
            score = item["score"]

            allocation_percentage = (
                score / total_score * 100
                if total_score > 0
                else 0
            )

            allocated_amount = (
                total_budget
                * allocation_percentage
                / 100
            )

            allocations.append({
                "channel_id": channel.get("channel_id"),
                "channel_name": channel.get("channel_name"),
                "channel_type": channel.get("channel_type"),
                "performance_score": score,
                "allocation_percentage": round(
                    allocation_percentage,
                    2,
                ),
                "allocated_budget": round(
                    allocated_amount,
                    2,
                ),
                "roas": round(
                    float(channel.get("roas", 0) or 0),
                    2,
                ),
                "ctr": round(
                    float(channel.get("ctr", 0) or 0),
                    2,
                ),
                "cpc": round(
                    float(channel.get("cpc", 0) or 0),
                    2,
                ),
            })

        allocations.sort(
            key=lambda item: item["allocation_percentage"],
            reverse=True,
        )

        return {
            "total_budget": round(total_budget, 2),
            "allocated_budget": round(
                sum(
                    item["allocated_budget"]
                    for item in allocations
                ),
                2,
            ),
            "channels": allocations,
        }