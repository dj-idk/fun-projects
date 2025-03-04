"""
An interactive cli number guessing game.
"""

import random


def main():
    random_number = random.randint(1, 100)

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

    choice = None
    guesses = 0

    difficulty = input("Enter your choice: ")

    try:
        difficulty = int(difficulty)
        if difficulty == 1:
            guesses = 10
            choice = "Easy"
        elif difficulty == 2:
            guesses = 5
            choice = "Medium"
        elif difficulty == 3:
            guesses = 3
            choice = "Hard"
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            return
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        return

    print(
        f"""
        Great! You have selected the {choice} difficulty level.
        You have {guesses} guesses. Let's start the game!
        """
    )

    attempts = 0

    while guesses > 0:
        user_guess = input("Enter your guess: ")
        attempts += 1
        try:
            user_guess = int(user_guess)
            if user_guess > random_number:
                print(f"Incorrect! The number is less than {user_guess}.")
            elif user_guess < random_number:
                print(f"Incorrect! The number is greater than {user_guess}.")
            else:
                print(
                    f"🎉 Congratulations! You guessed the correct number in {attempts} attempts."
                )
                return
            guesses -= 1
        except ValueError:
            print("Please enter a valid number.")

    print(
        f"\n😢 I'm sorry! You failed to guess the correct number in {attempts} attempts."
    )
    print(f"The correct number was {random_number}.")


if __name__ == "__main__":
    main()
