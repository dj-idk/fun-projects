import random
import time
import threading
import json

GAME_REPORT = "scores.json"


class ScoreTracker:
    def __init__(self, file=GAME_REPORT):
        self.file = file
        self.data = self.load_file()
        self.best_score = self.data.get("best_score", 0)

    def load_file(self):
        try:
            with open(self.file, "r") as input_file:
                return json.load(input_file)
        except (json.JSONDecodeError, IOError):
            print(
                "Warning: Could not read JSON file, initializing an empty score list."
            )
            return {"best_score": 0, "records": []}

    def save_data(self):
        try:
            with open(self.file, "w") as output_file:
                json.dump(self.data, output_file, indent=4)
        except IOError:
            print("Error: Could not save records to file.")

    def create_record(self, attempts, elapsed_time):
        attempts_weight = 10
        time_weight = 0.1
        c = 1
        try:
            new_id = (
                max((record["id"] for record in self.data["records"]), default=0) + 1
            )
            new_record = {
                "id": new_id,
                "attempts": attempts,
                "elapsed_time": elapsed_time,
                "score": round(
                    (
                        1
                        / (
                            (attempts * attempts_weight)
                            + (elapsed_time * time_weight)
                            + c
                        )
                    )
                    * 1000
                ),
            }
            self.data["records"].append(new_record)
            self.save_data()
            return new_record
        except Exception as e:
            print(f"Error creating record: {e}")
            return None

    def update_best_record(self, record):
        try:
            if record and record["score"] > self.best_score:
                self.best_score = record["score"]
                self.data["best_score"] = self.best_score  # Save best score in data
                self.save_data()
        except Exception as e:
            print(f"Error updating best score: {e}")

    def notify_new_best_score(self, record):
        if record and record["score"] > self.best_score:
            print(f"\n🎉 Congratulations! You just set a new record: {record['score']}")


def update_timer(start_time, stop_event):
    """Continuously update the timer while the game is running."""
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(
            "\033[s\033[H\033[KElapsed Time: {:.1f} seconds\033[u".format(elapsed_time),
            end="",
            flush=True,
        )
        time.sleep(0.1)


def main():
    random_number = random.randint(1, 100)
    score_tracker = ScoreTracker()

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print(
        """
        Please select the difficulty level:
        1. Easy (10 chances)
        2. Medium (5 chances)
        3. Hard (3 chances)                    
    """
    )

    difficulty = input("Enter your choice: ")

    try:
        difficulty = int(difficulty)
        if difficulty == 1:
            guesses = 10
        elif difficulty == 2:
            guesses = 5
        elif difficulty == 3:
            guesses = 3
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            return
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        return

    print(f"\nGreat! You have selected difficulty level with {guesses} attempts.")
    print("Let's start the game!\n")

    attempts = 0
    start_time = time.time()
    stop_event = threading.Event()

    print("\033[H\033[J", end="", flush=True)  # Clear the console

    timer_thread = threading.Thread(target=update_timer, args=(start_time, stop_event))
    timer_thread.daemon = True
    timer_thread.start()

    while guesses > 0:
        print("\033[2;0H\033[K", end="", flush=True)  # Move cursor for input
        user_guess = input("Enter your guess: ")
        attempts += 1

        try:
            user_guess = int(user_guess)
            print("\033[3;0H\033[K", end="", flush=True)  # Move cursor for feedback
            if user_guess > random_number:
                print(f"Incorrect! The number is less than {user_guess}.")
            elif user_guess < random_number:
                print(f"Incorrect! The number is greater than {user_guess}.")
            else:
                print(
                    f"🎉 Congratulations! You guessed the correct number in {attempts} attempts."
                )
                elapsed_time = time.time() - start_time
                print(f"Total time taken: {elapsed_time:.1f} seconds.")
                stop_event.set()
                new_record = score_tracker.create_record(attempts, elapsed_time)
                score_tracker.update_best_record(new_record)
                score_tracker.notify_new_best_score(new_record)
                return
            guesses -= 1

        except ValueError:
            print("\033[3;0H\033[K", end="", flush=True)
            print("Please enter a valid number.")

    elapsed_time = time.time() - start_time
    new_record = score_tracker.create_record(attempts, elapsed_time)
    stop_event.set()
    print(
        f"\n😢 I'm sorry! You failed to guess the correct number in {attempts} attempts."
    )
    print(f"The correct number was {random_number}.")
    print(f"Total time taken: {elapsed_time:.1f} seconds.")


if __name__ == "__main__":
    while True:
        main()
        play_again = input("Write any word that starts with y to play again: ")
        if not play_again.lower().startswith("y"):
            break
