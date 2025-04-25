from flask import Blueprint, request, jsonify
from ..db import get_favorites_collection
from datetime import datetime
from flask_login import current_user

favorites_bp = Blueprint('favorites', __name__)
collection = get_favorites_collection()

@favorites_bp.route("/", methods=["GET"])
def get_favorites():
    user_id = current_user.id if current_user.is_authenticated else "test-user"
    items = list(collection.find({"user_id": user_id}, {"_id": 0}))
    return jsonify(items)

@favorites_bp.route("/", methods=["POST"])
def add_favorite():
    data = request.get_json()

    # 这里我们允许最少只带 name 和 instructions （ingredients optional）
    if not all(k in data for k in ("name", "instructions")):
        return jsonify({"error": "Missing fields in favorite data"}), 400

    favorite = {
        "name": data["name"],
        "ingredients": data.get("ingredients", []),  # ingredients可以是空
        "instructions": data["instructions"],
        "added_on": datetime.utcnow().isoformat(),
        "user_id": current_user.id if current_user.is_authenticated else "test-user"
    }

    collection.insert_one(favorite)
    return jsonify({"message": "Item added successfully"}), 201

@favorites_bp.route("/<string:name>", methods=["DELETE"])
def delete_favorite(name):
    user_id = current_user.id if current_user.is_authenticated else "test-user"
    result = collection.delete_one({"name": name, "user_id": user_id})
    if result.deleted_count:
        return jsonify({"message": f"Deleted {name}"}), 200
    return jsonify({"error": "Item not found"}), 404
