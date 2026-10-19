
import random

words = ["python", "computer", "programming", "keyboard", "internet"]
# secret_word = "cat"
secret_word = random.choice(words)

guessed_letters = set()
attempts_left = 6

hangman_stages = [
    """
     +---+
     |   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =========
    """
]

print("Welcome to Hangman!")
print("Guess the hidden word, one letter at a time.")

while attempts_left > 0:
    print(hangman_stages[6 - attempts_left])

    display_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("Word:", display_word)
    print("Used letters:", ", ".join(sorted(guessed_letters)) or "None")
    print("Attempts left:", attempts_left)

    if all(letter in guessed_letters for letter in secret_word):
        print("\nCongratulations! You won!")
        break

    guess = input("Enter one letter: ").lower().strip()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single letter.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter!")
        continue

    guessed_letters.add(guess)

    if guess not in secret_word:
        attempts_left -= 1
        print("Wrong guess!")

else:
    print(hangman_stages[6])
    print("\nGame over! You ran out of attempts.")
    print("The hidden word was:", secret_word)
