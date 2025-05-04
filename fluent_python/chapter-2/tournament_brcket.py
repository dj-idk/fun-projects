
def generate_tournament_bracket(team_entries):
    """
    Generates a tournament bracket for a given list of teams.

    Args:
        team_entries (list): A list of teams, which can be string, tuple, dict or a list.
    Returns:
        list: A list of tuples representing the first-round matchups.
    """
    teams = []
    
    # Extract team information using pattern matching
    for team_entry in team_entries:
        match team_entry:
            case str():
                teams.append((team_entry, 0))
            case (name, seed):
                try:
                    seed = int(seed)
                except (ValueError, TypeError):
                    seed = 0
                teams.append((name, seed))
            case (name, seed, *_):
                try:
                    seed = int(seed)
                except (ValueError, TypeError):
                    seed = 0
                teams.append((name, seed))
            case [name, *_]:
                teams.append((name, 0))
            case {"name": name, "seed": seed, **extra}:
                try:
                    seed = int(seed)
                except (ValueError, TypeError):
                    seed = 0
                teams.append((name, seed))
            case {"name": name, **extra}:
                teams.append((name, 0))
            case _:
                print(f"Invalid team entry: {team_entry}")
                continue

    teams.sort(key=lambda x: -x[1])

    matchups = []
    n = len(teams)
    for i in range(n // 2):
        matchups.append((teams[i][0], teams[n-i-1][0]))
    
    return matchups

teams = [
    "Alpha Team",
    ("Beta Squad", 2),
    {"name": "Gamma Force", "seed": 1, "players": ["Alex", "Sam", "Jordan"], "region": "North"},
    ["Delta Crew", "Taylor", "Morgan", "Casey"],
    ("Epsilon Group", 3, "international", "first-time"),
    {"name": "Omega Unit", "region": "East", "seed": 2, "previous_rank": 3},
    "Zeta Team",
    ["Theta Squad", "Riley", "Quinn"],
    {"name": "Iota Fighters", "seed": 4, "coach": "Dr. Smith", "wins": 12, "losses": 3},
    ("Kappa Clan", 1, "defending champion"),
    ["Lambda Legion", "Avery", "Blake", "Cameron", "Dakota"],
    "Mu Marauders",
    ("Nu Ninjas", 3, "fan favorite"),
    {"name": "Xi Xecutioners", "seed": 2, "region": "West", "style": "aggressive"},
    ["Omicron Outlaws", "Emerson", "Finley", "Gray"],
    "Pi Punishers",
    ("Rho Raiders", 4, "underdog"),
    {"name": "Sigma Stars", "seed": 1, "region": "South", "consecutive_appearances": 5},
    ["Tau Titans", "Harper", "Indigo", "Jamie"],
    "Upsilon United",
    ("Phi Phoenixes", 2, "comeback story"),
    {"name": "Chi Champions", "seed": 3, "players": ["Kennedy", "London", "Monroe"], "sponsor": "TechCorp"},
    ["Psi Predators", "Noel", "Ocean", "Parker"],
    "Omega Warriors",
    ("Digamma Destroyers", 4, "wildcard"),
    {"name": "Koppa Killers", "seed": 3, "region": "Central", "mascot": "Dragon"},
    ["Sampi Slayers", "Quinn", "River", "Skyler"],
    "Heta Heroes",
    ("San Saviors", 1, "crowd favorite"),
    {"name": "Qoppa Quake", "seed": 2, "coach": "Prof. Johnson", "training_facility": "Mountain Base"},
    ["Stigma Strikers", "Taylor", "Unison", "Valentine"],
    "Wau Warriors"
]

bracket = generate_tournament_bracket(teams)
print(bracket)