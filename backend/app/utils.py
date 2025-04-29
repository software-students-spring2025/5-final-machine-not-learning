def extract_ingredients(cocktail):
    """
    Extract the ingredients from the cocktail dictionary.
    
    This function looks for keys like `strIngredient1`, `strIngredient2`, ..., `strIngredient15`
    and collects the corresponding ingredient names. It returns a list of ingredients in lowercase.
    """

    ingredients = []
    #loop through the ingredient keys (1 to 15) and collect non-empty ingredients
    for i in range(1, 16):
        ing = cocktail.get(f"strIngredient{i}")
        if ing:
            ingredients.append(ing.strip().lower())
    return ingredients

def match_cocktails_smart(cocktails, owned):
    """
    Match cocktails based on the owned ingredients and return a list of matches.
    
    This function compares the ingredients of each cocktail with the list of owned ingredients.
    It allows up to 2 missing ingredients and sorts the result based on the number of matched ingredients.
    """

    result = []

    #loop through each cocktail and compare its ingredients to the owned ingredients
    for c in cocktails:
        ings = extract_ingredients(c)
        matched = [i for i in ings if i in owned]
        missing = [i for i in ings if i not in owned]

        #allow up to 2 missing ingredients
        if len(matched) >= 2 and len(missing) <= 2:
            result.append({
                "name": c["strDrink"],
                "ingredients": ings,
                "matched": matched,
                "missing": missing,
                "instructions": c["strInstructions"],
                "image": c["strDrinkThumb"]
            })

    #sort by match quality: more matched ingredients come first
    result.sort(key=lambda x: (-len(x["matched"]), len(x["missing"])))
    return result
