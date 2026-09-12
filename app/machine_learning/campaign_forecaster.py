from datetime import date, timedelta

import numpy as np
from sklearn.linear_model import LinearRegression

from app.extensions import db
from app.models import CampaignPerformance


class CampaignForecaster:

    @staticmethod
    def forecast_campaign(campaign_id, days=7):
        records = (
            CampaignPerformance.query
            .filter_by(campaign_id=campaign_id)
            .order_by(CampaignPerformance.performance_date)
            .all()
        )

        if len(records) < 3:
            return {
                "campaign_id": campaign_id,
                "error": "At least 3 historical performance records are required."
            }

        dates = [
            record.performance_date
            for record in records
        ]

        impressions = np.array(
            [record.impressions for record in records],
            dtype=float,
        )

        clicks = np.array(
            [record.clicks for record in records],
            dtype=float,
        )

        conversions = np.array(
            [record.conversions for record in records],
            dtype=float,
        )

        spend = np.array(
            [float(record.spend) for record in records],
            dtype=float,
        )

        revenue = np.array(
            [float(record.revenue) for record in records],
            dtype=float,
        )

        X = np.arange(len(records)).reshape(-1, 1)

        future_X = np.arange(
            len(records),
            len(records) + days,
        ).reshape(-1, 1)

        def predict(values):
            model = LinearRegression()
            model.fit(X, values)

            predictions = model.predict(future_X)

            return np.maximum(predictions, 0)

        predicted_impressions = predict(impressions)
        predicted_clicks = predict(clicks)
        predicted_conversions = predict(conversions)
        predicted_spend = predict(spend)
        predicted_revenue = predict(revenue)

        forecast = []

        last_date = dates[-1]

        for index in range(days):
            forecast_date = (
                last_date + timedelta(days=index + 1)
            )

            forecast_impressions = int(
                round(predicted_impressions[index])
            )

            forecast_clicks = int(
                round(predicted_clicks[index])
            )

            forecast_conversions = int(
                round(predicted_conversions[index])
            )

            forecast_spend = round(
                float(predicted_spend[index]),
                2,
            )

            forecast_revenue = round(
                float(predicted_revenue[index]),
                2,
            )

            ctr = (
                forecast_clicks
                / forecast_impressions
                * 100
                if forecast_impressions > 0
                else 0
            )

            roas = (
                forecast_revenue
                / forecast_spend
                if forecast_spend > 0
                else 0
            )

            forecast.append({
                "date": forecast_date.isoformat(),
                "impressions": forecast_impressions,
                "clicks": forecast_clicks,
                "conversions": forecast_conversions,
                "spend": forecast_spend,
                "revenue": forecast_revenue,
                "ctr": round(ctr, 2),
                "roas": round(roas, 2),
            })

        return {
            "campaign_id": campaign_id,
            "historical_records": len(records),
            "forecast_days": days,
            "forecast": forecast,
        }

    @staticmethod
    def forecast_all_campaigns(days=7):
        campaign_ids = (
            db.session.query(
                CampaignPerformance.campaign_id
            )
            .distinct()
            .all()
        )

        results = []

        for row in campaign_ids:
            result = CampaignForecaster.forecast_campaign(
                row[0],
                days,
            )

            if "forecast" in result:
                results.append(result)

        return results