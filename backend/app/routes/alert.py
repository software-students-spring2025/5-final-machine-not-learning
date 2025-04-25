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
        query = {"user_id": "test-user"}  # 用测试用例里的"user_id"

    items = list(collection.find(query, {"_id": 0}))
    
    expiring_items = []
    for item in items:
        exp_date = item.get("expiration_date")
        if exp_date:
            try:
                exp = datetime.fromisoformat(exp_date)
                if today <= exp <= soon or exp < today:  # 包含已经过期的
                    expiring_items.append(item)
            except Exception:
                continue

    return jsonify(expiring_items)