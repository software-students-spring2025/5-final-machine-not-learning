from . import mongo

def get_inventory_collection():
    """
    Retrieve the inventory collection from the MongoDB database.

    This function returns the 'inventory' collection from the connected MongoDB instance.
    It's used to perform operations on the inventory data stored in the database.
    """

    return mongo.db.inventory

def get_favorites_collection():
    """
    Retrieve the favorites collection from the MongoDB database.

    This function returns the 'favorites' collection from the connected MongoDB instance.
    It's used to perform operations on the user's favorite items stored in the database.
    """
    
    return mongo.db.favorites
