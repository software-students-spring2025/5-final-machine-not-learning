# import requests

# def get_all_cocktails():
#     url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a"
#     all_recipes = []
#     for ch in "abcdefghijklmnopqrstuvwxyz":
#         res = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={ch}")
#         data = res.json()
#         if data["drinks"]:
#             all_recipes.extend(data["drinks"])
#     return all_recipes

import json
from pathlib import Path

#initialize a global variable to store cached cocktail data
cocktail_cache = []

def get_all_cocktails():
    """
    Retrieve all cocktails from the cache or the cached file.

    This function checks if the cocktail cache is populated. If so, it returns the cached data.
    Otherwise, it loads the cocktail data from a JSON file (`cocktail_cache.json`) and caches it.
    
    Returns:
        list: A list of all cocktails loaded from the cache or file.
    
    Raises:
        FileNotFoundError: If the `cocktail_cache.json` file is missing.
    """

    global cocktail_cache

    if cocktail_cache:
        return cocktail_cache

    #get the current directory path where the script is located
    CURRENT_DIR = Path(__file__).parent
    cache_path = CURRENT_DIR / "cocktail_cache.json"

    if not cache_path.exists():
        raise FileNotFoundError("File not found")

    with cache_path.open("r", encoding="utf-8") as f:
        cocktail_cache = json.load(f)

    return cocktail_cache

