from functools import partial
from random import choice, choices, shuffle


def scale_recipe_dict(recipe_dict: list, scale: float):
    scaled_recipe = []

    for item in recipe_dict:
        for name, details in item.items():
            scaled_item = {
                name: {
                    "amount": details["amount"] * scale,
                    "unit": details["unit"],
                    "notes": details["notes"],
                }
            }
            scaled_recipe.append(scaled_item)

    return scaled_recipe


double_recipe_dict = partial(scale_recipe_dict, scale=2)
half_recipe_dict = partial(scale_recipe_dict, scale=0.5)
family_size_dict = partial(scale_recipe_dict, scale=4)


def create_random_recipes(ingredients: list):
    num_ingredients = choice(range(1, 7))
    selected_ingredients = choices(ingredients, k=num_ingredients)

    random_recipe = [
        {name: {"amount": amount, "unit": unit, "notes": notes}}
        for name, amount, unit, *notes in selected_ingredients
    ]

    return random_recipe


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

random_recipe = create_random_recipes(ingredients)
print(f"Original recipe:{random_recipe}")
print("Doubled recipe:")
print(double_recipe_dict(random_recipe))
print("Family Recipe:")
print(family_size_dict(random_recipe))
print("Half recipe:")
print(half_recipe_dict(random_recipe))
