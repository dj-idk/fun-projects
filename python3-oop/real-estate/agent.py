from typed_property import (
    HouseRental,
    ApartmentRental,
    HousePurchase,
    ApartmentPurchase,
)
from type import get_valid_input


class Agent:
    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase,
    }

    def __init__(self):
        self.property_list = []

    def add_property(self):
        property_type = get_valid_input(
            "What type of property would you like to add (house/apartment)? ",
            ("house", "apartment"),
        ).lower()
        payment_type = get_valid_input(
            "What type of property is it (rental/purchase)? ", ("rental", "purchase")
        ).lower()
        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))

    def display_properties(self):
        for property in self.property_list:
            property.display()
