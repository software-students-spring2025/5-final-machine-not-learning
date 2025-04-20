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

cocktail_cache = []

def get_all_cocktails():
    global cocktail_cache
    if cocktail_cache:
        return cocktail_cache

    CURRENT_DIR = Path(__file__).parent
    cache_path = CURRENT_DIR / "cocktail_cache.json"

    if not cache_path.exists():
        raise FileNotFoundError("File not found")

    with cache_path.open("r", encoding="utf-8") as f:
        cocktail_cache = json.load(f)

    return cocktail_cache

