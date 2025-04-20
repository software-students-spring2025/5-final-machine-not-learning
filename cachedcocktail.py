import requests
import json

all_drinks = []

for ch in "abcdefghijklmnopqrstuvwxyz":
    print(f"Fetching drinks starting with {ch}...")
    res = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={ch}")
    data = res.json()
    if data and data["drinks"]:
        all_drinks.extend(data["drinks"])

with open("cocktail_cache.json", "w", encoding="utf-8") as f:
    json.dump(all_drinks, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(all_drinks)} cocktails to cocktail_cache.json")