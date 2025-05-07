from collections import namedtuple, deque
from random import randint
from time import sleep
import json
import os
from operator import attrgetter

Player = namedtuple("Player", ["name", "wins", "losses", "average_surviaval_time"])


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


def save_game_stats(players, winner):
    """
    Save game statistics to a JSON file.

    Args:
        players (list): List of player names who participated in the game
        winner (str): Name of the player who won the game
    """
    stats_file = "player_stats.json"
    stats_data = {}

    if os.path.exists(stats_file):
        try:
            with open(stats_file, "r") as f:
                stats_data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: Stats file corrupted. Creating new stats.")

    for player in players:
        survival_time = 0
        if player in stats_data:
            player_stats = stats_data[player]

            if player == winner:
                player_stats["wins"] += 1
            else:
                player_stats["losses"] += 1

            games_played = player_stats["wins"] + player_stats["losses"]
            current_avg = player_stats["average_survival_time"]

            if player == winner:
                survival_time = len(players) * 2
            else:
                survival_time = players.index(player) + 1

            new_avg = (
                (current_avg * (games_played - 1)) + survival_time
            ) / games_played
            player_stats["average_survival_time"] = round(new_avg, 2)

        else:
            if player == winner:
                stats_data[player] = {
                    "wins": 1,
                    "losses": 0,
                    "average_survival_time": len(players) * 2,
                }
            else:
                stats_data[player] = {
                    "wins": 0,
                    "losses": 1,
                    "average_survival_time": players.index(player) + 1,
                }

    try:
        with open(stats_file, "w") as f:
            json.dump(stats_data, f, indent=4)
        print(f"Game statistics saved to {stats_file}")

        display_leaderboard(stats_data)
    except IOError:
        print("Error: Could not save game statistics.")


def display_leaderboard(stats_data):
    """
    Display a leaderboard of players sorted by wins.

    Args:
        stats_data (dict): Dictionary containing player statistics
    """
    if not stats_data:
        print("No player statistics available.")
        return

    players = []
    for name, stats in stats_data.items():
        player = Player(
            name=name,
            wins=stats["wins"],
            losses=stats["losses"],
            average_surviaval_time=stats["average_survival_time"],
        )
        players.append(player)

    sorted_players = sorted(players, key=attrgetter("wins"), reverse=True)

    print("\n===== LEADERBOARD =====")
    print(f"{'Name':<15} {'Wins':<6} {'Losses':<8} {'Avg Survival':<12}")
    print("-" * 40)

    for player in sorted_players[:5]:
        print(
            f"{player.name:<15} {player.wins:<6} {player.losses:<8} {player.average_surviaval_time:<12.2f}"
        )
    print("=" * 40)


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

    winner = player_circle[0]
    print(f"\nCongratulations! {winner} is the winner!")

    save_game_stats(players, winner)


if __name__ == "__main__":
    while True:
        players = get_player_names()
        start_game(players)

        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != "y":
            print("Thanks for playing!")
            break
