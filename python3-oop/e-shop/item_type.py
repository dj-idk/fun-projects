from collections import namedtuple

Dimension = namedtuple("Dimension", ["length", "width", "height"])


class PhysicalItem:
    """A physical item with weight, dimensions, shipping cost, fragility, storage location, and handling instructions."""

    def __init__(
        self,
        weight,
        dimensions: Dimension,
        shipping_cost,
        fragile,
        storage_location,
        handling_instructions,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.weight = weight
        self.dimensions = dimensions
        self.shipping_cost = shipping_cost
        self.fragile = fragile
        self.storage_location = storage_location
        self.handling_instructions = handling_instructions

    def display(self):
        """Display the physical item details."""
        super().display()
        print("Physical Item Details:")
        print("------------------------")
        print(f"Weight: {self.weight}")
        print(f"Dimensions: {self.dimensions}")
        print(f"Shipping Cost: ${self.shipping_cost}")
        print(f"Fragile: {self.fragile}")
        print(f"Storage Location: {self.storage_location}")
        print(f"Handling Instructions: {self.handling_instructions}")
        print("------------------------")
        print()

    def calculate_shipping_cost(self, distance, expedicted=False):
        """Calculate the shipping cost based on distance."""
        self.shipping_cost = self.weight * 0.5 * distance
        if expedicted:
            self.shipping_cost *= 1.2
            return self.shipping_cost
        return self.shipping_cost

    def get_packaging_requirements(self):
        """Get the packaging requirements based of weight and dimensions."""
        if (
            self.weight > 10
            and self.dimensions.length > 5
            and self.dimensions.width > 5
            and self.dimensions.height > 5
        ):
            return "Large"
        elif (
            self.weight > 5
            and self.dimensions.length > 3
            and self.dimensions.width > 3
            and self.dimensions.height > 3
        ):
            return "Medium"
        else:
            return "Small"

    @staticmethod
    def prompt_init():
        """Prompt the user to initialize a PhysicalItem object."""
        return dict(
            weight=float(input("Enter the weight of the item: ")),
            dimensions=Dimension(
                length=float(input("Enter the length of the item: ")),
                width=float(input("Enter the width of the item: ")),
                height=float(input("Enter the height of the item: ")),
            ),
            shipping_cost=float(input("Enter the shipping cost: ")),
            fragile=(input("Is the item fragile? (yes/no): ").lower() == "yes"),
            storage_location=input("Enter the storage location: "),
            handling_instructions=input("Enter the handling instructions: "),
        )


class DigitalItem:
    """A digital item with file size, download link, compatibility, license type, version, and release date."""

    def __init__(
        self,
        file_size,
        download_link,
        compatability,
        license_type,
        version,
        release_date,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.file_size = file_size
        self.download_link = download_link
        self.compatability = compatability
        self.license_type = license_type
        self.version = version
        self.release_date = release_date

    def display(self):
        """Display the digital item details."""
        super().display()
        print("Digital Item Details:")
        print("------------------------")
        print(f"File Size: {self.file_size}")
        print(f"Download Link: {self.download_link}")
        print(f"Compatibility: {self.compatability}")
        print(f"License Type: {self.license_type}")
        print(f"Version: {self.version}")
        print(f"Release Date: {self.release_date}")
        print("------------------------")
        print()

    def generate_download_link(self, user_id):
        """Generate a download link based on user ID."""
        return f"{self.download_link}?user_id={user_id}"

    def check_compatibility(self, device_type):
        """Check if the item is compatible with the specified device type."""
        return device_type.lower() in self.compatability.lower()

    def update_version(self, new_version, new_link, new_size):
        """Update the version, download link, and file size of the digital item."""
        self.version = new_version
        self.download_link = new_link
        self.file_size = new_size
        print("Version updated successfully.")

    @staticmethod
    def prompt_init():
        """Prompt the user to initialize a DigitalItem object."""
        return dict(
            file_size=float(input("Enter the file size of the item: ")),
            download_link=input("Enter the download link: "),
            compatability=input("Enter the compatability (comma-separated): ").split(
                ","
            ),
            license_type=input("Enter the license type: "),
            version=input("Enter the version: "),
            release_date=input("Enter the release date (YYYY-MM-DD): "),
        )
