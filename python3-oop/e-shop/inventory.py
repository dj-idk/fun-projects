from typed_product import (
    PhysicalBook,
    DigitalBook,
    PhysicalElectronic,
    DigitalElectronic,
    PhysicalClothing,
)
from item_type import PhysicalItem, DigitalItem


def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        else:
            print("Invalid option. Please try again.")


class Inventory:
    """Class to manage the inventory of products in the e-shop."""

    product_map = {
        ("book", "physical"): PhysicalBook,
        ("book", "digital"): DigitalBook,
        ("electronic", "physical"): PhysicalElectronic,
        ("electronic", "digital"): DigitalElectronic,
        ("clothing", "physical"): PhysicalClothing,
    }

    def __init__(self):
        """Initialize an empty inventory."""
        self.products = []

    def add_product(self):
        """Add a new product to the inventory based on user input."""
        product_category = get_valid_input(
            "What type of product would you like to add (book/electronic/clothing)? ",
            ("book", "electronic", "clothing"),
        ).lower()

        if product_category == "clothing":
            product_type = "physical"
            print("Note: Clothing items can only be physical.")
        else:
            product_type = get_valid_input(
                f"What type of {product_category} is it (physical/digital)? ",
                ("physical", "digital"),
            ).lower()

        ProductClass = self.product_map.get((product_category, product_type))

        if ProductClass:
            init_args = ProductClass.prompt_init()
            product = ProductClass(**init_args)
            self.products.append(product)
            print(
                f"{product_category.capitalize()} added to inventory with SKU: {product.sku}"
            )
        else:
            print(
                f"Sorry, {product_type} {product_category} is not a valid product type."
            )

    def remove_product(self, sku):
        """Remove a product from the inventory by SKU."""
        for i, product in enumerate(self.products):
            if product.sku == sku:
                removed = self.products.pop(i)
                print(f"Removed {removed.name} from inventory.")
                return True
        print(f"No product with SKU {sku} found in inventory.")
        return False

    def search_by_name(self, name):
        """Search products by name (case-insensitive partial match)."""
        results = [p for p in self.products if name.lower() in p.name.lower()]
        return results

    def search_by_category(self, category):
        """Search products by category."""
        results = [p for p in self.products if p.category.lower() == category.lower()]
        return results

    def search_by_price_range(self, min_price, max_price):
        """Search products within a price range."""
        results = [p for p in self.products if min_price <= p.price <= max_price]
        return results

    def display_all_products(self):
        """Display all products in the inventory."""
        if not self.products:
            print("Inventory is empty.")
            return

        print(f"\n{'=' * 50}")
        print(f"INVENTORY - {len(self.products)} products")
        print(f"{'=' * 50}")

        for i, product in enumerate(self.products, 1):
            print(f"\n--- Product {i} ---")
            product.display()
            print()

    def get_physical_products(self):
        """Get all physical products in the inventory."""

        return [p for p in self.products if isinstance(p, PhysicalItem)]

    def get_digital_products(self):
        """Get all digital products in the inventory."""

        return [p for p in self.products if isinstance(p, DigitalItem)]

    def calculate_total_inventory_value(self):
        """Calculate the total value of all products in inventory."""
        total_value = sum(
            p.price * (1 if not hasattr(p, "in_stock") else p.in_stock)
            for p in self.products
        )
        return total_value

    def generate_download_links_for_user(self, user_id):
        """Generate download links for a user's digital purchases."""

        digital_products = [p for p in self.products if isinstance(p, DigitalItem)]

        if not digital_products:
            print("No digital products in inventory.")
            return []

        links = []
        for product in digital_products:
            link = product.generate_download_link(user_id)
            links.append((product.name, link))

        return links

    def calculate_shipping_for_order(self, product_skus, distance):
        """Calculate total shipping cost for an order."""
        total_shipping = 0
        products_found = []

        for sku in product_skus:
            product = next((p for p in self.products if p.sku == sku), None)

            if product is None:
                print(f"Warning: Product with SKU {sku} not found.")
                continue

            if not isinstance(product, PhysicalItem):
                print(f"Note: {product.name} is a digital item with no shipping cost.")
                continue

            shipping_cost = product.calculate_shipping_cost(distance)
            total_shipping += shipping_cost
            products_found.append((product.name, shipping_cost))

        return total_shipping, products_found

    def display_search_results(self, results):
        """Display search results in a formatted way."""
        if not results:
            print("No matching products found.")
            return

        print(f"\n{'=' * 50}")
        print(f"SEARCH RESULTS - {len(results)} products found")
        print(f"{'=' * 50}")

        for i, product in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"SKU: {product.sku}")
            print(f"Name: {product.name}")
            print(f"Price: ${product.price:.2f}")
            print(f"Category: {product.category}")

            if hasattr(product, "file_size"):
                print("Type: Digital")
            else:
                print("Type: Physical")

        print(f"\n{'=' * 50}")


def main():
    """Main function to demonstrate the inventory system."""
    inventory = Inventory()

    while True:
        print("\n=== E-Shop Inventory Management ===")
        print("1. Add a product")
        print("2. Remove a product")
        print("3. Display all products")
        print("4. Search products")
        print("5. Calculate inventory value")
        print("6. Calculate shipping for an order")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == "1":
            inventory.add_product()
        elif choice == "2":
            sku = input("Enter the SKU of the product to remove: ")
            inventory.remove_product(sku)
        elif choice == "3":
            inventory.display_all_products()
        elif choice == "4":
            print("\n--- Search Options ---")
            print("1. Search by name")
            print("2. Search by category")
            print("3. Search by price range")
            search_choice = input("Enter search option (1-3): ")

            if search_choice == "1":
                name = input("Enter product name to search: ")
                results = inventory.search_by_name(name)
                inventory.display_search_results(results)
            elif search_choice == "2":
                category = input("Enter category to search: ")
                results = inventory.search_by_category(category)
                inventory.display_search_results(results)
            elif search_choice == "3":
                try:
                    min_price = float(input("Enter minimum price: "))
                    max_price = float(input("Enter maximum price: "))
                    results = inventory.search_by_price_range(min_price, max_price)
                    inventory.display_search_results(results)
                except ValueError:
                    print("Invalid price. Please enter numeric values.")
            else:
                print("Invalid search option.")
        elif choice == "5":
            total_value = inventory.calculate_total_inventory_value()
            print(f"Total inventory value: ${total_value:.2f}")
        elif choice == "6":
            skus_input = input("Enter SKUs of products (comma-separated): ")
            skus = [sku.strip() for sku in skus_input.split(",")]
            try:
                distance = float(input("Enter shipping distance (miles): "))
                total_cost, items = inventory.calculate_shipping_for_order(
                    skus, distance
                )

                print("\n--- Shipping Calculation ---")
                for name, cost in items:
                    print(f"{name}: ${cost:.2f}")
                print(f"Total shipping cost: ${total_cost:.2f}")
            except ValueError:
                print("Invalid distance. Please enter a numeric value.")
        elif choice == "7":
            print("Exiting inventory management system.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
