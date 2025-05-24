from item_type import PhysicalItem, DigitalItem
from items import Book, Electronic, Clothing


class PhysicalBook(PhysicalItem, Book):
    def __init__(self, cover_type, condition, **kwargs):
        super().__init__(**kwargs)
        self.cover_type = cover_type
        self.condition = condition

    def display(self):
        super().display()
        print(f"Cover Type: {self.cover_type}")
        print(f"Condition: {self.condition}")

    def calculate_shipping_by_weight(self):
        base_rate = 2.0
        return base_rate + (self.weight * 0.5)

    @staticmethod
    def prompt_init():
        init = {}
        init.update(PhysicalItem.prompt_init())
        init.update(Book.prompt_init())
        init["cover_type"] = input("Enter cover type (Hardcover/Paperback): ")
        init["condition"] = input("Enter condition (New/Used/Like New): ")
        return init


class DigitalBook(DigitalItem, Book):
    def __init__(self, drm_protected, supported_devices, **kwargs):
        super().__init__(**kwargs)
        self.drm_protected = drm_protected
        self.supported_devices = supported_devices

    def display(self):
        super().display()
        print(f"DRM Protected: {self.drm_protected}")
        print(f"Supported Devices: {', '.join(self.supported_devices)}")

    def check_device_compatibility(self, device):
        return device in self.supported_devices

    @staticmethod
    def prompt_init():
        init = {}
        init.update(DigitalItem.prompt_init())
        init.update(Book.prompt_init())
        init["drm_protected"] = (
            input("Is the book DRM protected? (yes/no): ").lower() == "yes"
        )
        devices = input("Enter supported devices (comma separated): ")
        init["supported_devices"] = [device.strip() for device in devices.split(",")]
        return init


class PhysicalElectronic(PhysicalItem, Electronic):
    def __init__(self, requires_assembly, includes_batteries, **kwargs):
        super().__init__(**kwargs)
        self.requires_assembly = requires_assembly
        self.includes_batteries = includes_batteries

    def display(self):
        super().display()
        print(f"Requires Assembly: {self.requires_assembly}")
        print(f"Includes Batteries: {self.includes_batteries}")

    def calculate_shipping_with_insurance(self, distance):
        base_shipping = self.calculate_shipping_cost(distance)
        insurance_rate = 0.01
        insurance_cost = self.price * insurance_rate
        return base_shipping + insurance_cost

    @staticmethod
    def prompt_init():
        init = {}
        init.update(PhysicalItem.prompt_init())
        init.update(Electronic.prompt_init())
        init["requires_assembly"] = (
            input("Requires assembly? (yes/no): ").lower() == "yes"
        )
        init["includes_batteries"] = (
            input("Includes batteries? (yes/no): ").lower() == "yes"
        )
        return init


class DigitalElectronic(DigitalItem, Electronic):
    def __init__(self, activation_key, subscription_period, **kwargs):
        super().__init__(**kwargs)
        self.activation_key = activation_key
        self.subscription_period = subscription_period

    def display(self):
        super().display()
        print(f"Activation Key: {self.activation_key}")
        print(f"Subscription Period: {self.subscription_period} months")

    def generate_activation_key(self):
        import uuid

        self.activation_key = str(uuid.uuid4())
        return self.activation_key

    def extend_subscription(self, months):
        self.subscription_period += months
        print(
            f"Subscription extended by {months} months. New period: {self.subscription_period} months."
        )

    @staticmethod
    def prompt_init():
        init = {}
        init.update(DigitalItem.prompt_init())
        init.update(Electronic.prompt_init())
        init["activation_key"] = (
            input("Enter activation key (leave blank to generate): ")
            or "To be generated"
        )
        init["subscription_period"] = int(
            input("Enter subscription period in months (0 for lifetime): ")
        )
        return init


class PhysicalClothing(PhysicalItem, Clothing):
    def __init__(self, returnable, gift_wrapping, **kwargs):
        super().__init__(**kwargs)
        self.returnable = returnable
        self.gift_wrapping = gift_wrapping

    def display(self):
        super().display()
        print(f"Returnable: {self.returnable}")
        print(f"Gift Wrapping Available: {self.gift_wrapping}")

    def calculate_shipping_by_weight(self):
        base_rate = 3.0
        return base_rate + (self.weight * 0.3)

    @staticmethod
    def prompt_init():
        init = {}
        init.update(PhysicalItem.prompt_init())
        init.update(Clothing.prompt_init())
        init["returnable"] = (
            input("Is the item returnable? (yes/no): ").lower() == "yes"
        )
        init["gift_wrapping"] = (
            input("Is gift wrapping available? (yes/no): ").lower() == "yes"
        )
        return init
