from flask import Blueprint, request, jsonify
from ..db import get_inventory_collection
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)
collection = get_inventory_collection()

@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    items = list(collection.find({}, {"_id": 0}))
    return jsonify(items)

@inventory_bp.route("/", methods=["POST"])
def add_item():
    data = request.get_json()
    data["added_on"] = datetime.utcnow().isoformat()
    collection.insert_one(data)
    return jsonify({"message": "Item added successfully"}), 201

@inventory_bp.route("/<string:name>", methods=["DELETE"])
def delete_item(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        return jsonify({"message": f"Deleted {name}"}), 200
    return jsonify({"error": "Item not found"}), 404

