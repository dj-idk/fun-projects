import requests
import json
import sys


def fetch_user_activities(username):
    if username:
        try:
            activities = requests.get(f"https://api.github.com/users/{username}/events")
            return activities.text
        except Exception as e:
            return e


def display_user_activity(activities):
    print("User activities:")
    activities = json.loads(activities)
    for activity in activities:
        print(f"Event type: {activity['type']}")
        print(f"Repository: {activity['repo']['name']}")
        print(f"Date: {activity['created_at']}")
        print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a username.")
        sys.exit(1)
    if sys.argv[1]:
        activities = fetch_user_activities(sys.argv[1])
        display_user_activity(activities)
