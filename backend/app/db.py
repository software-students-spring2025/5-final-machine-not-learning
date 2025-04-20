from . import mongo

def get_inventory_collection():
    return mongo.db.inventory
