last_id = 0


class Product:
    """Represents a product in a store."""

    def __init__(self, name, price, description, category, in_stock=True, **kwargs):
        super().__init__(**kwargs)
        global last_id
        last_id += 1
        self.sku = last_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.in_stock = in_stock

    def display(self):
        """Displays the product details."""
        print("Product Details:")
        print(f"Product ID: {self.sku}")
        print(f"Product Name: {self.name}")
        print(f"Product Description: {self.description}")
        print(f"Product Category: {self.category}")
        print(f"Product Stock Status: {self.in_stock}")
        print()

    def update_price(self, new_price):
        """Updates the product price."""
        self.price = new_price
        print(f"Price updated to {self.price}")

    def update_stock(self, new_stock_status):
        """Updates the product stock status."""
        self.in_stock = new_stock_status
        print(f"Stock status updated to {self.in_stock}")

    def get_basic_info(self):
        """Returns a basic info string of the product."""
        return f"Product ID: {self.sku}, Name: {self.name}, Price: {self.price}"

    @staticmethod
    def prompt_init():
        """Prompts the user to enter product details and returns them as a dictionary."""
        return dict(
            name=input("Enter product name: "),
            price=float(input("Enter product price: $")),
            description=input("Enter product description: "),
            category=input("Enter product category: "),
            in_stock=input("Is the product in stock (yes/no)? ").lower() == "yes",
        )
