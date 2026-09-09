from app.extensions import db
from app.models import Brand


class BrandService:
    """Business logic for Brand Management."""

    @staticmethod
    def get_all():
        brands = Brand.query.order_by(Brand.brand_name).all()

        return [
            {
                "brand_id": brand.brand_id,
                "brand_code": brand.brand_code,
                "brand_name": brand.brand_name,
                "industry": brand.industry,
                "website": brand.website,
            }
            for brand in brands
        ]

    @staticmethod
    def get_by_id(brand_id):
        brand = db.session.get(Brand, brand_id)

        if not brand:
            return None

        return {
            "brand_id": brand.brand_id,
            "brand_code": brand.brand_code,
            "brand_name": brand.brand_name,
            "industry": brand.industry,
            "website": brand.website,
        }

    @staticmethod
    def create(data):
        brand = Brand(**data)

        db.session.add(brand)
        db.session.commit()

        return BrandService.get_by_id(brand.brand_id)

    @staticmethod
    def update(brand_id, data):
        brand = db.session.get(Brand, brand_id)

        if not brand:
            return None

        for key, value in data.items():
            setattr(brand, key, value)

        db.session.commit()

        return BrandService.get_by_id(brand.brand_id)

    @staticmethod
    def delete(brand_id):
        brand = db.session.get(Brand, brand_id)

        if not brand:
            return False

        db.session.delete(brand)
        db.session.commit()

        return True