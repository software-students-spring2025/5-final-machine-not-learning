from flask import Blueprint, jsonify
from ..db import get_inventory_collection
from datetime import datetime, timedelta

alert_bp = Blueprint('alert', __name__)
collection = get_inventory_collection()

@alert_bp.route("/soon", methods=["GET"])
def get_expiring_soon():
    today = datetime.utcnow()
    soon = today + timedelta(days=5)

    items = list(collection.find({}, {"_id": 0}))
    expiring_items = []

    for item in items:
        exp_date = item.get("expiration_date")
        if exp_date:
            try:
                exp = datetime.fromisoformat(exp_date)
                if today <= exp <= soon:
                    expiring_items.append(item)
            except Exception:
                continue

    return jsonify(expiring_items)
