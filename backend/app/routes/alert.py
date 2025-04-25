# app/routes/alert.py
from flask import Blueprint, jsonify
from ..db import get_inventory_collection
from datetime import datetime, timedelta
from flask_login import current_user

alert_bp = Blueprint('alert', __name__)
collection = get_inventory_collection()

@alert_bp.route("/soon", methods=["GET"])
def get_expiring_and_expired():
    today = datetime.utcnow()
    soon = today + timedelta(days=5)

    items = list(collection.find({"user_id": current_user.id}, {"_id": 0}))
    expiring_soon = []
    expired = []

    for item in items:
        exp_date = item.get("expiration_date")
        if exp_date:
            try:
                exp = datetime.fromisoformat(exp_date)
                if exp < today:
                    expired.append(item)
                elif today <= exp <= soon:
                    expiring_soon.append(item)
            except Exception:
                continue

    return jsonify({
        "expired": expired,
        "expiring_soon": expiring_soon
    })
