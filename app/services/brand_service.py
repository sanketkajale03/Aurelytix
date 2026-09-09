from app.extensions import db
from app.models import Brand


class BrandService:

    @staticmethod
    def get_all():
        brands = Brand.query.order_by(
            Brand.created_at.desc()
        ).all()

        return [
            {
                "brand_id": brand.brand_id,
                "advertiser_id": brand.advertiser_id,
                "brand_name": brand.brand_name,
                "brand_code": brand.brand_code,
                "category": brand.category,
                "status": brand.status,
            }
            for brand in brands
        ]

    @staticmethod
    def get_by_id(brand_id):
        brand = db.session.get(Brand, brand_id)

        if brand is None:
            return None

        return {
            "brand_id": brand.brand_id,
            "advertiser_id": brand.advertiser_id,
            "brand_name": brand.brand_name,
            "brand_code": brand.brand_code,
            "category": brand.category,
            "status": brand.status,
        }

    @staticmethod
    def create(data):
        brand = Brand(
            advertiser_id=data["advertiser_id"],
            brand_name=data["brand_name"],
            brand_code=data["brand_code"],
            category=data.get("category"),
            status=data.get("status", "ACTIVE"),
        )

        db.session.add(brand)
        db.session.commit()

        return BrandService.get_by_id(brand.brand_id)

    @staticmethod
    def update(brand_id, data):
        brand = db.session.get(Brand, brand_id)

        if brand is None:
            return None

        allowed_fields = [
            "advertiser_id",
            "brand_name",
            "brand_code",
            "category",
            "status",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(brand, field, data[field])

        db.session.commit()

        return BrandService.get_by_id(brand_id)

    @staticmethod
    def delete(brand_id):
        brand = db.session.get(Brand, brand_id)

        if brand is None:
            return False

        db.session.delete(brand)
        db.session.commit()

        return True