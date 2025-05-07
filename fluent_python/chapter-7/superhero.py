from operator import attrgetter
from collections import namedtuple
from functools import partial

SuperHero = namedtuple("SuperHero", ["name", "primary_attribute", "level", "weakness"])


def sort_by_attribute(collection, /, attr, reverse, *attrs):
    return sorted(collection, key=attrgetter(attr, *attrs), reverse=reverse)


sort_by_primary_attribute = partial(
    lambda collection, *attrs, reverse=False: sort_by_attribute(
        collection, "primary_attribute", reverse, *attrs
    )
)


heroes = [
    SuperHero("Superman", "Strength", 100, "Radiation"),
    SuperHero("Batman", "Intelligence", 90, "Darkness"),
    SuperHero("Spiderman", "Agility", 85, "Web"),
    SuperHero("Wonder Woman", "Speed", 95, "Flying"),
    SuperHero("Hulk", "Strength", 105, "Bruises"),
    SuperHero("Thor", "Intelligence", 98, "Fire"),
    SuperHero("Captain America", "Strength", 88, "Frost"),
    SuperHero("Iron Man", "Intelligence", 92, "Radiation"),
    SuperHero("Black Widow", "Agility", 87, "Web"),
    SuperHero("Deadpool", "Strength", 102, "Poison"),
]

sorted_heroes = sort_by_primary_attribute(heroes, "level", reverse=True)

for hero in sorted_heroes:
    print(f"{hero.name}: {hero.primary_attribute} - Level: {hero.level}")
