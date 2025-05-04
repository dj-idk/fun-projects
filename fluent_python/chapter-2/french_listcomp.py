from collections import namedtuple

Card = namedtuple("Card", ["rank", "suit"])
ranks = [*range(2,11), "Jack", "Queen", "King", "Ace"]
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

deck = [Card(rank, suit) for rank in ranks for suit in suits]

print(deck)