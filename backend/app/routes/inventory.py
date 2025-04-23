from flask import Blueprint, request, jsonify
from ..db import get_inventory_collection
from datetime import datetime
from flask_login import current_user

inventory_bp = Blueprint('inventory', __name__)
collection = get_inventory_collection()

@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    user_id = current_user.id if current_user.is_authenticated else "test-user"
    items = list(collection.find({"user_id": user_id}, {"_id": 0}))
    return jsonify(items)

@inventory_bp.route("/", methods=["POST"])
def add_item():
    data = request.get_json()
    data["added_on"] = datetime.utcnow().isoformat()
    data["user_id"] = current_user.id if current_user.is_authenticated else "test-user"
    collection.insert_one(data)
    print(f"added {data}")
    return jsonify({"message": "Item added successfully"}), 201

@inventory_bp.route("/<string:name>", methods=["DELETE"])
def delete_item(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        return jsonify({"message": f"Deleted {name}"}), 200
    return jsonify({"error": "Item not found"}), 404

