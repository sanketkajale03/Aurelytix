from app.extensions import db
from app.models import AudienceSegment


class AudienceService:

    @staticmethod
    def get_all():
        audiences = AudienceSegment.query.order_by(
            AudienceSegment.created_at.desc()
        ).all()

        return [
            {
                "audience_segment_id": audience.audience_segment_id,
                "segment_name": audience.segment_name,
                "age_min": audience.age_min,
                "age_max": audience.age_max,
                "gender": audience.gender,
                "income_level": audience.income_level,
                "interests": audience.interests,
                "segment_description": audience.segment_description,
            }
            for audience in audiences
        ]

    @staticmethod
    def get_by_id(audience_segment_id):
        audience = db.session.get(
            AudienceSegment,
            audience_segment_id
        )

        if audience is None:
            return None

        return {
            "audience_segment_id": audience.audience_segment_id,
            "segment_name": audience.segment_name,
            "age_min": audience.age_min,
            "age_max": audience.age_max,
            "gender": audience.gender,
            "income_level": audience.income_level,
            "interests": audience.interests,
            "segment_description": audience.segment_description,
        }

    @staticmethod
    def create(data):
        audience = AudienceSegment(
            segment_name=data["segment_name"],
            age_min=data.get("age_min"),
            age_max=data.get("age_max"),
            gender=data.get("gender"),
            income_level=data.get("income_level"),
            interests=data.get("interests"),
            segment_description=data.get("segment_description"),
        )

        db.session.add(audience)
        db.session.commit()

        return AudienceService.get_by_id(
            audience.audience_segment_id
        )

    @staticmethod
    def update(audience_segment_id, data):
        audience = db.session.get(
            AudienceSegment,
            audience_segment_id
        )

        if audience is None:
            return None

        allowed_fields = [
            "segment_name",
            "age_min",
            "age_max",
            "gender",
            "income_level",
            "interests",
            "segment_description",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(audience, field, data[field])

        db.session.commit()

        return AudienceService.get_by_id(audience_segment_id)

    @staticmethod
    def delete(audience_segment_id):
        audience = db.session.get(
            AudienceSegment,
            audience_segment_id
        )

        if audience is None:
            return False

        db.session.delete(audience)
        db.session.commit()

        return True