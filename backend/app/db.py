from . import mongo

def get_inventory_collection():
    return mongo.db.inventory

def get_favorites_collection():
    return mongo.db.favorites
