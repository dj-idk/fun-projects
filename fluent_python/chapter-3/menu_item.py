from collections import OrderedDict
from enum import Enum
import json
import sys


class Category(str, Enum):
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"


class MenuTracker:
    def __init__(self):
        self.menu_items = OrderedDict()

    def __setitem__(self, name, item_data):
        self.menu_items[name] = item_data

    def add_item(self, name: str, price: int, category: Category):
        self.menu_items[name] = {
            "price": price,
            "category": category,
            "available": True,
        }
        return self.menu_items[name]

    def update_item(self, name: str, price: str):
        updated_item = self.menu_items.get(name)
        if not updated_item:
            raise KeyError("Item you're looking for was not found !!")
        updated_item["price"] = price
        return updated_item

    def change_availability(self, name: str):
        updated_item = self.menu_items.get(name)
        if not updated_item:
            raise KeyError("Item you're looking for was not found")
        updated_item["available"] = not updated_item["available"]
        return updated_item

    def read_all_items(self):
        return self.menu_items.items()

    def read_category_items(self, category: str):
        category_items = []
        for name, item in self.menu_items.items():
            if item["category"] == category:
                category_items.append({"name": name, "price": item["price"]})
        return {category: category_items}

    def remove_item(self, name: str):
        item = self.menu_items.get(name)
        if not item:
            raise KeyError("Item you're looking for was not found")
        self.menu_items.pop(name)
        print(f"{name} has been successfully removed")

    def move_to_end(self, name: str):
        self.menu_items.move_to_end(name)

    def move_to_first(self, name: str):
        self.menu_items.move_to_end(name, last=False)

    def save_to_file(self):
        with open("menu.json", "w+") as fp:
            json.dump(list(self.menu_items.items()), fp)

    def load_from_file(self):
        with open("menu.json", "r") as fp:
            items = json.load(fp)
            self.menu_items = OrderedDict(items)
        return self.menu_items


def display_menu():
    print("\n===== Restaurant Menu Tracker =====")
    print("1. Add a new menu item")
    print("2. Update item price")
    print("3. Change item availability")
    print("4. List all menu items")
    print("5. List items by category")
    print("6. Remove a menu item")
    print("7. Move item to end of menu")
    print("8. Move item to beginning of menu")
    print("9. Save menu to file")
    print("10. Load menu from file")
    print("11. Exit")
    print("===================================")


def print_item(name, item):
    availability = "Available" if item["available"] else "Not Available"
    print(f"- {name}: ${item['price']:.2f} ({item['category']}) - {availability}")


def main():
    tracker = MenuTracker()

    # Add some initial items for testing
    tracker.add_item("Caesar Salad", 8.99, Category.APPETIZER)
    tracker.add_item("Steak", 24.99, Category.MAIN_COURSE)
    tracker.add_item("Cheesecake", 6.99, Category.DESSERT)
    tracker.add_item("Soup of the Day", 5.99, Category.APPETIZER)

    while True:
        display_menu()
        choice = input("Enter your choice (1-11): ")

        try:
            if choice == "1":
                name = input("Enter item name: ")
                price = float(input("Enter price: "))
                print("Categories: 1. Appetizer, 2. Main Course, 3. Dessert")
                cat_choice = input("Enter category number: ")

                if cat_choice == "1":
                    category = Category.APPETIZER
                elif cat_choice == "2":
                    category = Category.MAIN_COURSE
                elif cat_choice == "3":
                    category = Category.DESSERT
                else:
                    print("Invalid category choice!")
                    continue

                tracker.add_item(name, price, category)
                print(f"Added {name} to the menu!")

            elif choice == "2":
                name = input("Enter item name to update: ")
                price = float(input("Enter new price: "))
                tracker.update_item(name, price)
                print(f"Updated price for {name}!")

            elif choice == "3":
                name = input("Enter item name to toggle availability: ")
                item = tracker.change_availability(name)
                status = "available" if item["available"] else "unavailable"
                print(f"{name} is now {status}!")

            elif choice == "4":
                print("\n===== Current Menu =====")
                for name, item in tracker.read_all_items():
                    print_item(name, item)

            elif choice == "5":
                print("Categories: 1. Appetizer, 2. Main Course, 3. Dessert")
                cat_choice = input("Enter category number: ")

                if cat_choice == "1":
                    category = Category.APPETIZER
                elif cat_choice == "2":
                    category = Category.MAIN_COURSE
                elif cat_choice == "3":
                    category = Category.DESSERT
                else:
                    print("Invalid category choice!")
                    continue

                result = tracker.read_category_items(category)
                print(f"\n===== {category} Items =====")
                for item in result[category]:
                    print(f"- {item['name']}: ${item['price']:.2f}")

            elif choice == "6":
                name = input("Enter item name to remove: ")
                tracker.remove_item(name)

            elif choice == "7":
                name = input("Enter item name to move to end: ")
                tracker.move_to_end(name)
                print(f"Moved {name} to the end of the menu!")

            elif choice == "8":
                name = input("Enter item name to move to beginning: ")
                tracker.move_to_first(name)
                print(f"Moved {name} to the beginning of the menu!")

            elif choice == "9":
                tracker.save_to_file()
                print("Menu saved to menu.json!")

            elif choice == "10":
                tracker.load_from_file()
                print("Menu loaded from menu.json!")

            elif choice == "11":
                print("Thank you for using Restaurant Menu Tracker!")
                sys.exit(0)

            else:
                print("Invalid choice! Please enter a number between 1 and 11.")

        except KeyError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: Invalid input - {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
