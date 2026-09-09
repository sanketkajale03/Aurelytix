from flask import Blueprint, jsonify, request

from app.services.brand_service import BrandService


brands_bp = Blueprint("brands", __name__)


@brands_bp.get("/api/brands")
def get_brands():
    brands = BrandService.get_all()
    return jsonify(brands), 200


@brands_bp.get("/api/brands/<int:brand_id>")
def get_brand(brand_id):
    brand = BrandService.get_by_id(brand_id)

    if brand is None:
        return jsonify({
            "error": "Brand not found"
        }), 404

    return jsonify(brand), 200


@brands_bp.post("/api/brands")
def create_brand():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "advertiser_id",
        "brand_name",
        "brand_code",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    brand = BrandService.create(data)

    return jsonify(brand), 201


@brands_bp.put("/api/brands/<int:brand_id>")
def update_brand(brand_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    brand = BrandService.update(brand_id, data)

    if brand is None:
        return jsonify({
            "error": "Brand not found"
        }), 404

    return jsonify(brand), 200


@brands_bp.delete("/api/brands/<int:brand_id>")
def delete_brand(brand_id):
    deleted = BrandService.delete(brand_id)

    if not deleted:
        return jsonify({
            "error": "Brand not found"
        }), 404

    return jsonify({
        "message": "Brand deleted successfully"
    }), 200