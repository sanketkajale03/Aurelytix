from flask import Blueprint, jsonify, request

from app.services.brand_service import BrandService

brands_bp = Blueprint("brands", __name__)


@brands_bp.get("/api/brands")
def get_brands():
    return jsonify(BrandService.get_all()), 200


@brands_bp.get("/api/brands/<int:brand_id>")
def get_brand(brand_id):
    brand = BrandService.get_by_id(brand_id)

    if brand is None:
        return jsonify({"error": "Brand not found"}), 404

    return jsonify(brand), 200


@brands_bp.post("/api/brands")
def create_brand():
    data = request.get_json(silent=True) or {}

    brand = BrandService.create(data)

    return jsonify(brand), 201


@brands_bp.put("/api/brands/<int:brand_id>")
def update_brand(brand_id):
    data = request.get_json(silent=True) or {}

    brand = BrandService.update(brand_id, data)

    if brand is None:
        return jsonify({"error": "Brand not found"}), 404

    return jsonify(brand), 200


@brands_bp.delete("/api/brands/<int:brand_id>")
def delete_brand(brand_id):
    deleted = BrandService.delete(brand_id)

    if not deleted:
        return jsonify({"error": "Brand not found"}), 404

    return jsonify({"message": "Brand deleted successfully"}), 200