class Property:
    def __init__(self, square_feet="", beds="", baths="", **kwargs):
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.num_beds = beds
        self.num_baths = baths

    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print(f"square footage: {self.square_feet}")
        print(f"bedrooms: {self.num_beds}")
        print(f"bathrooms: {self.num_baths}")
        print()

    @staticmethod
    def prompt_init():
        return dict(
            square_feet=input("Enter square footage: "),
            beds=input("Enter number of bedrooms: "),
            baths=input("Enter number of bathrooms: "),
        )


class Apartment(Property):
    valid_laundaries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony="", laundry="", **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        super().display()
        print("APARTMENT DETAILS")
        print("================")
        print(f"balcony: {self.balcony}")
        print(f"laundry: {self.laundry}")
        print()

    @staticmethod
    def prompt_init():
        parent_init = Property.prompt_init()
        laundary = ""
        while laundary.lower() not in Apartment.valid_laundries:
            laundary = input("Enter laundry type (coin, ensuite, none): ")
        balcony = ""
        while balcony.lower() not in Apartment.valid_balconies:
            balcony = input("Enter balcony type (yes, no, solarium): ")
        parent_init.update(
            {
                "laundry": laundary,
                "balcony": balcony,
            }
        )
        return parent_init


class House(Property):
    valid_garages = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories="", garage="", fenced="", **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories

    def display(self):
        super().display()
        print("HOUSE DETAILS")
        print("==============")
        print(f"number of stories: {self.num_stories}")
        print(f"garage: {self.garage}")
        print(f"fenced: {self.fenced}")
        print()

    @staticmethod
    def prompt_init():
        parent_init = Property.prompt_init()
        garage = ""
        while garage.lower() not in House.valid_garages:
            garage = input("Enter garage type (attached, detached, none): ")
        fenced = ""
        while fenced.lower() not in House.valid_fenced:
            fenced = input("Enter fenced property (yes, no): ")
        num_stories = input("How many stories? ")
        parent_init.update(
            {
                "garage": garage,
                "fenced": fenced,
                "num_stories": num_stories,
            }
        )
        return parent_init
