from product import Product


class Electronic(Product):
    def __init__(
        self,
        warranty_period,
        power_consumption,
        manufacturer,
        model_number,
        technical_specs,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.warranty_period = warranty_period
        self.power_consumption = power_consumption
        self.manufacturer = manufacturer
        self.model_number = model_number
        self.technical_specs = technical_specs

    def display(self):
        super().display()
        print(f"Warranty Period: {self.warranty_period} years")
        print(f"Power Consumption: {self.power_consumption} watts")
        print(f"Manufacturer: {self.manufacturer}")
        print(f"Model Number: {self.model_number}")
        print(f"Technical Specs: {self.technical_specs}")

    def extend_warranty(self, months):
        self.warranty_period += months
        print(
            f"Warranty period extended by {months} months. New warranty period: {self.warranty_period} months."
        )

    def get_specs(self):
        return {
            "Warranty Period": self.warranty_period,
            "Power Consumption": self.power_consumption,
            "Manufacturer": self.manufacturer,
            "Model Number": self.model_number,
            "Technical Specs": self.technical_specs,
        }

    @staticmethod
    def prompt_init():
        init = Product.prompt_init()
        return dict(
            init,
            warranty_period=int(input("Enter the warranty period in months: ")),
            power_consumption=float(input("Enter the power consumption in watts: ")),
            manufacturer=input("Enter the manufacturer: "),
            model_number=input("Enter the model number: "),
            technical_specs=input("Enter technical specifications: "),
        )


class Book(Product):
    def __init__(
        self,
        author,
        pages,
        publisher,
        isbn,
        publication_date,
        genre,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.author = author
        self.pages = pages
        self.publisher = publisher
        self.isbn = isbn
        self.publication_date = publication_date
        self.genre = genre

    def display(self):
        super().display()
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages}")
        print(f"Publisher: {self.publisher}")
        print(f"ISBN: {self.isbn}")
        print(f"Publication Date: {self.publication_date}")
        print(f"Genre: {self.genre}")

    def get_book_details(self):
        return {
            "Author": self.author,
            "Pages": self.pages,
            "Publisher": self.publisher,
            "ISBN": self.isbn,
            "Publication Date": self.publication_date,
            "Genre": self.genre,
        }

    @staticmethod
    def prompt_init():
        init = Product.prompt_init()
        return dict(
            init,
            author=input("Enter the author: "),
            pages=int(input("Enter the number of pages: ")),
            publisher=input("Enter the publisher: "),
            isbn=input("Enter the ISBN: "),
            publication_date=input("Enter the publication date: "),
            genre=input("Enter the genre: "),
        )


class Clothing(Product):
    def __init__(
        self,
        size,
        material,
        care_instructions,
        color,
        gender,
        season,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.size = size
        self.material = material
        self.care_instructions = care_instructions
        self.color = color
        self.gender = gender
        self.season = season

    def display(self):
        super().display()
        print(f"Size: {self.size}")
        print(f"Material: {self.material}")
        print(f"Care Instructions: {self.care_instructions}")
        print(f"Color: {self.color}")
        print(f"Gender: {self.gender}")
        print(f"Season: {self.season}")

    def available_sizes(self):
        return [self.size]

    @staticmethod
    def prompt_init():
        init = Product.prompt_init()
        return dict(
            init,
            size=input("Enter the size (S, M, L, XL, etc.): "),
            material=input("Enter the material: "),
            care_instructions=input("Enter care instructions: "),
            color=input("Enter the color: "),
            gender=input("Enter the gender (Men, Women, Unisex): "),
            season=input("Enter the season (Summer, Winter, All-season): "),
        )
