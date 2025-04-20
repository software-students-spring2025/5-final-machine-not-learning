from datetime import datetime

def default_item():
    return {
        "name": "",
        "category": "",  # e.g. spirit, mixer, garnish
        "quantity": 1,
        "opened_on": datetime.utcnow().isoformat(),
        "expiration_date": None  # optional
    }
