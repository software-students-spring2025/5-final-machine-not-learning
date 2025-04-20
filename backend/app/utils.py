def extract_ingredients(cocktail):
    ingredients = []
    for i in range(1, 16):
        ing = cocktail.get(f"strIngredient{i}")
        if ing:
            ingredients.append(ing.strip().lower())
    return ingredients

def match_cocktails_smart(cocktails, owned):
    result = []

    for c in cocktails:
        ings = extract_ingredients(c)
        matched = [i for i in ings if i in owned]
        missing = [i for i in ings if i not in owned]

        # ✅ 允许最多缺 2 项
        if len(matched) >= 2 and len(missing) <= 2:
            result.append({
                "name": c["strDrink"],
                "ingredients": ings,
                "matched": matched,
                "missing": missing,
                "instructions": c["strInstructions"],
                "image": c["strDrinkThumb"]
            })

    # ✅ 排序：匹配度越高越靠前
    result.sort(key=lambda x: (-len(x["matched"]), len(x["missing"])))
    return result

