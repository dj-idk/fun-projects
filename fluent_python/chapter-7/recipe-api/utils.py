from operator import attrgetter, itemgetter
from functools import partial


def sort_recipes(recipes: list, key, reverse=False):
    """Sort recipes based on a given key"""
    try:
        return sorted(recipes, key=attrgetter(key), reverse=reverse)
    except AttributeError:
        return sorted(recipes, key=itemgetter(key), reverse=reverse)
    except TypeError:
        raise ValueError("Invalid key for sorting")


def filter_recipes(recipes: list, key, value):
    """Filter recipes based on attributes matching a value"""
    try:
        return [recipe for recipe in recipes if attrgetter(key)(recipe) == value]
    except AttributeError:
        raise ValueError(f"No attribute '{key}' found in recipes")


def get_recipe_ingredients(recipes: list, recipe_id):
    """Return a list of ingredients for a given recipe"""
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe.ingredients
        raise ValueError(f"No recipe found with ID {recipe_id}")
    return []


def scale_recipe_ingredients(ingredients: list, scale: float):
    """Scale the amount of ingredients by a given factor"""
    return [
        {
            "name": ingredient.get("name"),
            "amount": ingredient.get("amount") * scale,
            "unit": ingredient.get("unit"),
        }
        for ingredient in ingredients
    ]


double_recipe_ingredients = partial(scale_recipe_ingredients, scale=2)

half_recipe_ingredients = partial(scale_recipe_ingredients, scale=0.5)

sort_by_difficulty = partial(sort_recipes, key="difficulty", reverse=True)

sort_by_prep_time = partial(sort_recipes, key="prep_time")
