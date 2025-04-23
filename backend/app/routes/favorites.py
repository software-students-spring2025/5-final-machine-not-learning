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
    data["added_on"] = datetime.utcnow().isoformat()
    data["user_id"] = current_user.id if current_user.is_authenticated else "test-user"
    item = collection.insert_one(data)
    return jsonify({"message": "Item added successfully"}), 201


@favorites_bp.route("/<string:info>", methods=["DELETE"])
def delete_favorite(info):
    result = collection.delete_one({"info": info})
    if result.deleted_count:
        return jsonify({"message": f"Deleted {info}"}), 200
    return jsonify({"error": "Item not found"}), 404
