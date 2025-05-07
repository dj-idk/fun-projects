from enum import Enum

from colorama import Fore, Style, init

init(autoreset=True)


class SpellElement(str, Enum):
    FIRE = "Fire"
    WATER = "Water"
    EARTH = "Earth"
    AIR = "Air"
    ETHER = "Ether"


class Spell:

    def __init__(
        self, name: str, power_level: int, element: SpellElement, description: str
    ):
        self.name = name
        self.power_level = power_level
        self.element = element
        self.description = description

    def __str__(self):
        properties = f"{Style.BRIGHT}{self.name} Level {self.power_level}, Element: {self.element.value}, Description {self.description}"
        match self.element:
            case SpellElement.FIRE:
                return f"{Fore.RED} {properties}"
            case SpellElement.WATER:
                return f"{Fore.CYAN} {properties}"
            case SpellElement.EARTH:
                return f"{Fore.YELLOW} {properties}"
            case SpellElement.AIR:
                return f"{Fore.LIGHTWHITE_EX} {properties}"
            case SpellElement.ETHER:
                return f"{Fore.LIGHTGREEN_EX} {properties}"
            case _:
                print("Invalid Element.")

    def __call__(self):
        return str(self)


fireball = Spell("Fireball", 7, SpellElement.FIRE, "Hurls a ball of fire at the target")
ice_lance = Spell(
    "Ice Lance", 6, SpellElement.WATER, "Pierces enemies with a freezing lance"
)
stone_skin = Spell(
    "Stone Skin", 4, SpellElement.EARTH, "Hardens the caster's skin for protection"
)
wind_gust = Spell(
    "Wind Gust", 3, SpellElement.AIR, "Pushes enemies away with a strong gust"
)
arcane_missile = Spell(
    "Arcane Missile", 8, SpellElement.ETHER, "Fires homing magical missiles"
)

if __name__ == "__main__":
    print("Available spells:")
    for spell in [fireball, ice_lance, stone_skin, wind_gust, arcane_missile]:
        print(spell())
