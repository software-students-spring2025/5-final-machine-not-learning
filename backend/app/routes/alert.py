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

    if current_user.is_authenticated:
        query = {"user_id": current_user.id}
    else:
        query = {"user_id": "test-user"}

    items = list(collection.find(query, {"_id": 0}))
    
    expired = []
    expiring_soon = []

    for item in items:
        exp_date_str = item.get("expiration_date")
        if exp_date_str:
            try:
                exp = datetime.fromisoformat(exp_date_str[:10])
                if exp < today:
                    expired.append(item)
                elif today <= exp <= soon:
                    expiring_soon.append(item)
            except Exception as e:
                print(f"[ERROR PARSING DATE] {exp_date_str} => {e}")
                continue

    return jsonify({
        "expired": expired,
        "expiring_soon": expiring_soon
    })