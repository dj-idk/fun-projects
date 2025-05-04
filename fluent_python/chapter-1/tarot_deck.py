from collections import namedtuple
import random

Card = namedtuple("Card",["rank","suit"])

class TarotDeck:
    """ A deck of Tarot cards """
    major_arcana = [
        "The Fool", "The Magician", "The High Priestess", "The Empress",
        "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
        "Strength", "The Hermit", "Wheel of Fortune", "Justice",
        "The Hanged Man", "Death", "Temperance", "The Devil",
        "The Tower", "The Star", "The Moon", "The Sun",
        "Judgement", "The World"
    ]

    minor_arcana_ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                          'Page', 'Knight', 'Queen', 'King']
    minor_arcana_suits = ['wands', 'cups', 'swords', 'pentacles']
    def __init__(self):
        self._cards = [Card("Major",suit) for suit in self.major_arcana] + [Card(rank,suit) for rank in self.minor_arcana_ranks for suit in self.minor_arcana_suits]

    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self,position):
        return self._cards[position]
    
    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self, n=1):
        drawn = self._cards[:n]
        self._cards = self._cards[n:]
        return drawn
    
# Simulate a reading
deck = TarotDeck()
deck.shuffle()

spread = deck.draw(3)
positions = ["Past", "Present", "Future"]

print("🔮 3-Card Tarot Spread:")
for pos, card in zip(positions, spread):
    print(f"{pos}: {card.rank} of {card.suit}")