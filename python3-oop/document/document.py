class Cursor:
    def __init__(self, document):
        self.document = document
        self.position = 0

    def forward(self):
        if self.position < len(self.document.characters):
            self.position += 1

    def backward(self):
        if self.position > 0:
            self.position -= 1

    def home(self):
        while self.document.characters[self.position - 1] != "\n":
            self.backward()
            if self.position == 0:
                break

    def end(self):
        while (
            self.position < len(self.document.characters)
            and self.document.characters[self.position] != "\n"
        ):
            self.forward()


class Character:
    def __init__(self, character, bold=False, italic=False, underline=False):
        assert len(character) == 1
        self.character = character
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def __str__(self):
        return (
            f"\033[1m"
            if self.bold
            else (
                "" + f"\033[3m"
                if self.italic
                else (
                    "" + f"\033[4m"
                    if self.underline
                    else "" + self.character + "\033[0m"
                )
            )
        )


class Document:
    def __init__(self):
        self.characters = []
        self.cursor = Cursor(self)
        self.filename = ""

    def insert(self, character):
        if not hasattr(character, "character"):
            character = Character(character)
        self.characters.insert(self.cursor.position, character)
        self.cursor.forward()

    def delete(self):
        del self.characters[self.cursor.position]

    def save(self):
        with open(self.filename, "w") as file:
            file.write("".join(self.characters))

    @property
    def string(self):
        return "".join((str(c) for c in self.characters))
