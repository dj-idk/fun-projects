from collections import namedtuple
import random

card = namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    """A French deck of 52 cards"""

    ranks = [str(n) for n in range(2, 11)] + list({"Jack", "Queen", "King", "Ace"})
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

    def __init__(self):
        self._cards = [card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        """Shuffle the deck of cards"""

        random.shuffle(self._cards)
        return self


# Create a French deck and shuffle it

deck = FrenchDeck()
shuffled_deck = deck.shuffle()

# Draw a card from the shuffled deck
card = shuffled_deck[1]
print(f"You drew a {card.rank} of {card.suit}.")
