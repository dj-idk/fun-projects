"""
# Fetch and store activities
python github-tracker.py johndoe fetch

# Display stored activities
python github-tracker.py johndoe display

"""

import os
import json
import requests
import argparse
from datetime import datetime
from colorama import Fore, Style, init

import redis

redis_client = redis.Redis("localhost", db=1)


class GithubTracker:
    def __init__(self, file, username):
        self.file = file
        self.username = username
        self.data = self.load_file()
        self.redis_key = f"{self.username}_github_activities"

    def load_file(self):
        if not os.path.exists(self.file):
            print("No existing file found. Creating a new one.")
            return {
                "username": self.username,
                "date_added": datetime.now().isoformat(),
                "activities": [],
            }

        try:
            with open(self.file, "r") as in_file:
                return json.load(in_file)
        except json.JSONDecodeError:
            print("Error: JSON file is corrupted. Creating a new one.")
        except IOError:
            print("Error: Unable to read file.")

        return {
            "username": self.username,
            "date_added": datetime.now().isoformat(),
            "activities": [],
        }

    def save_file(self):
        try:
            if not self.data["activities"]:
                raise ValueError("No activities to save")
            with open(self.file, "w") as out_file:
                json.dump(self.data, out_file, indent=4)
        except IOError:
            print("Data file might be corrupt or missing.")

    def fetch_activities(self):
        try:

            url = f"https://api.github.com/users/{self.username}/events"
            response = requests.get(url)

            if response.status_code != 200:
                raise ValueError(f"Couldn't fetch activities for {self.username}")

            return response.json()
        except Exception as e:
            raise RuntimeError(f"Error while fetching activities: {e}")

    def format_activities(self, activities):
        try:
            formatted_activities = []

            for activity in activities:
                formatted_activity = {
                    "Event Type": activity.get("type", "Unknown"),
                    "Repository": activity.get("repo", {}).get("name", "Unknown"),
                    "Date": activity.get("created_at", "Unknown"),
                }
                formatted_activities.append(formatted_activity)

            return formatted_activities
        except Exception as e:
            raise RuntimeError(f"Error while formatting activities: {e}")

    def add_activities(self, activities):
        try:
            if not isinstance(activities, list):
                raise ValueError("Invalid activities format")

            prev_activities_set = {
                frozenset(activity.items()) for activity in self.data["activities"]
            }
            new_activities_set = {
                frozenset(activity.items()) for activity in activities
            }

            unique_new_activities = new_activities_set - prev_activities_set

            if not unique_new_activities:
                print("No new activities to add.")
                return

            self.data["activities"].extend(
                dict(activity) for activity in unique_new_activities
            )

            self.save_file()
            print(f"✅ Added {len(unique_new_activities)} new activities.")

        except Exception as e:
            raise RuntimeError(f"Error while adding activities: {e}")

    def display_activities(self):
        try:
            init(autoreset=True)

            color_map = {
                "PushEvent": Fore.GREEN,
                "PullRequestEvent": Fore.BLUE,
                "IssuesEvent": Fore.YELLOW,
                "ForkEvent": Fore.RED,
                "WatchEvent": Fore.MAGENTA,
            }

            activities = self.data.get("activities", [])
            if not activities:
                print(Fore.RED + "No activities found!")
                return

            print(Fore.CYAN + f"GitHub Activities for {self.username}:")
            print(Fore.CYAN + "=" * 50)

            for activity in activities:
                event_type = activity["Event Type"]
                repo = activity["Repository"]
                date = activity["Date"]

                color = color_map.get(event_type, Fore.WHITE)
                print(f"{color}[{event_type}] {Style.BRIGHT}{repo} - {date}")

            print(Fore.CYAN + "=" * 50)
        except Exception as e:
            raise RuntimeError(f"Error while displaying activities: {e}")

    def cache_activities(self, activities):
        try:
            activities_json = json.dumps(activities)

            redis_client.setex(self.redis_key, 300, activities_json)
            print("✅ Activities were cached successfully.")
        except Exception as e:
            raise RuntimeError(f"Error while caching activities: {e}")

    def check_cache(self):
        try:
            cached_data = redis_client.get(self.redis_key)
            if not cached_data:
                print(f"{self.username} activities are not cached yet.")
                return None

            ttl = redis_client.ttl(self.redis_key)
            if ttl == -1:
                print("⚠️ Cached activities exist but do not have an expiry time.")
            elif ttl == -2:
                print("❌ Cached activities have expired.")
                return None
            else:
                print(f"Using cached activities, expires in: {ttl} seconds")

            return json.loads(cached_data)

        except Exception as e:
            raise RuntimeError(f"Error while checking for cached activities: {e}")


def main():
    parser = argparse.ArgumentParser(description="GitHub Activity Tracker")
    parser.add_argument("username", help="GitHub username")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("fetch", help="Fetch GitHub activities and save them")

    subparsers.add_parser("display", help="Show stored GitHub activities")

    args = parser.parse_args()

    file_name = f"{args.username}_activities.json"

    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            json.dump(
                {
                    "username": args.username,
                    "date_added": datetime.now().isoformat(),
                    "activities": [],
                },
                f,
                indent=4,
            )

    tracker = GithubTracker(file_name, args.username)

    if args.command == "fetch":
        cached_activities = tracker.check_cache()

        if cached_activities:
            activities = cached_activities
        else:
            activities = tracker.fetch_activities()
            tracker.cache_activities(activities)

        formatted_activities = tracker.format_activities(activities)
        tracker.add_activities(formatted_activities)
        print(f"✅ Activities fetched and saved in {file_name}!")

    elif args.command == "display":
        tracker.display_activities()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
