def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        else:
            print("Invalid option. Please try again.")


class Purchase:
    def __init__(self, price="", taxes="", **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        super().display()
        print("PURCHASE DETAILS")
        print(f"Price: {self.price}")
        print(f"Estimated Taxes: {self.taxes}")

    @staticmethod
    def prompt_init():
        return dict(
            price=input("What's the selling price? "),
            taxes=input("What are the estimated taxes?  "),
        )


class Rental:
    def __init__(self, furnished="", utilities="", rent="", **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.utilities = utilities
        self.rent = rent

    def display(self):
        super().display()
        print("RENTAL DETAILS")
        print(f"Furnished: {self.furnished}")
        print(f"Utilities: {self.utilities}")
        print(f"Rent: {self.rent}")

    @staticmethod
    def prompt_init():
        return dict(
            furnished=get_valid_input("Is the property furnished? ", ("yes", "no")),
            utilities=input("What are the estimated utilities? "),
            rent=input("What is the monthly rent?  "),
        )
