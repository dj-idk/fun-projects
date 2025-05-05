from collections import deque
from random import randint
from time import sleep


def get_player_names():
    """
    Retrieves player names and returns a list of strings,
    """
    players = []
    while True:
        print("Welcome to Hot Potato Game!")
        names = input("Enter player names separated by commas:").split(",")
        if len(names) < 2:
            print("We need at least two players to start the game!")
            continue
        for name in names:
            if len(name.strip()) < 2:
                print("Please enter a valid name")
                break
            players.append(name.strip())

        return players


def start_game(players):
    """Takes a list of player names and starts the hot potato game"""
    player_circle = deque(players)
    print(
        f"Starting game with {len(player_circle)} players: {', '.join(player_circle)}"
    )

    round_num = 1
    while len(player_circle) > 1:
        print(f"\nRound {round_num} begins!")

        num_of_passes = randint(1, 10)
        print(f"The potato will be passed {num_of_passes} times!")

        for i in range(num_of_passes):
            player_circle.rotate(1)
            print(f"Passing potato... now with {player_circle[0]}")
            sleep(0.2)

        eliminated_player = player_circle.popleft()
        print(f"{eliminated_player} is holding the potato and is eliminated!")

        round_num += 1

    print(f"\nCongratulations! {player_circle[0]} is the winner!")


if __name__ == "__main__":
    while True:
        players = get_player_names()
        start_game(players)

        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != "y":
            print("Thanks for playing!")
            break
