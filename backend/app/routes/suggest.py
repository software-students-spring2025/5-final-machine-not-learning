from flask import Blueprint, jsonify
from ..db import get_inventory_collection
from ..cocktaildb import get_all_cocktails
from ..utils import match_cocktails_smart
from flask_login import current_user

suggest_bp = Blueprint('suggest', __name__)
inventory_col = get_inventory_collection()

@suggest_bp.route("/available", methods=["GET"])
def suggest_from_inventory():
    user_id = current_user.id if current_user.is_authenticated else "test-user"
    inventory_items = list(inventory_col.find({"user_id": user_id}, {"_id": 0, "name": 1}))
    owned_ingredients = [item["name"].lower() for item in inventory_items]

    cocktails = get_all_cocktails()
    matched = match_cocktails_smart(cocktails, owned_ingredients)

    return jsonify({"matched": matched, "user_logged": current_user.is_authenticated})

