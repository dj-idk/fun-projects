def organize_ingredients(ingredients):
    """
    Organizes recipe ingredients by category.

    Args:
        ingredients: List of ingredient tuples

    Returns:
        Dictionary with categories as keys and lists of ingredient details as values
    """
    organized_ingredients = {}

    for ingredient in ingredients:
        match ingredient:
            case (name, amount, unit, category, *extra):
                is_special = "special" in extra
                notes = [note for note in extra if note != "special"]

            case (name, amount, unit, category):
                is_special = False
                notes = []

            case (name, amount, unit):
                category = "miscellaneous"
                is_special = False
                notes = []

            case _:
                print(f"Warning: Unexpected ingredient format: {ingredient}")
                continue

        category_list = organized_ingredients.setdefault(category, [])

        ingredient_details = {
            "name": name,
            "amount": amount,
            "unit": unit,
            "notes": notes,
            "special": is_special,
        }

        combined = False
        for existing in category_list:
            if existing["name"] == name and existing["unit"] == unit:
                existing["amount"] += amount
                for note in notes:
                    if note not in existing["notes"]:
                        existing["notes"].append(note)
                existing["special"] |= is_special
                combined = True
                break

        if not combined:
            category_list.append(ingredient_details)

    return organized_ingredients


ingredients = [
    ("all-purpose flour", 2, "cups", "dry"),
    ("cake flour", 1.5, "cups", "dry", "sifted"),
    ("eggs", 3, "units", "protein", "room temperature"),
    ("egg whites", 2, "units", "protein", "whipped"),
    ("whole milk", 1, "cup", "liquid", "cold"),
    ("buttermilk", 0.5, "cup", "liquid", "cultured"),
    ("salt", 1, "tsp"),
    ("kosher salt", 0.5, "tsp", "seasoning", "finishing"),
    ("granulated sugar", 1.5, "cups", "dry", "sweetener"),
    ("brown sugar", 0.75, "cup", "dry", "sweetener", "packed"),
    ("vanilla extract", 1, "tbsp", "flavor", "special"),
    ("almond extract", 0.5, "tsp", "flavor"),
    ("butter", 1, "cup", "fat", "unsalted", "softened"),
    ("vegetable oil", 0.25, "cup", "fat"),
    ("baking powder", 2, "tsp", "leavening"),
    ("baking soda", 0.5, "tsp", "leavening"),
    ("chocolate chips", 1, "cup", "add-in", "semi-sweet"),
    ("walnuts", 0.5, "cup", "add-in", "chopped", "optional"),
    ("cinnamon", 1, "tsp", "spice"),
    ("nutmeg", 0.25, "tsp", "spice", "freshly grated"),
    ("lemon zest", 1, "tbsp", "flavor", "fresh"),
    ("cream cheese", 8, "oz", "dairy", "softened", "for frosting"),
    ("powdered sugar", 2, "cups", "dry", "sweetener", "sifted", "for frosting"),
    ("heavy cream", 0.25, "cup", "liquid", "cold", "whipped"),
    ("strawberries", 1, "cup", "fruit", "sliced", "for garnish"),
    ("food coloring", 3, "drops", "special", "red"),
]

organized_ingredients = organize_ingredients(ingredients)
print(organized_ingredients)
