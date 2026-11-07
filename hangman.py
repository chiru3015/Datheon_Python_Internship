
import random

# Step 1: Word list
words = [
    "python", "computer", "science", "programming",
    "developer", "keyboard", "internet", "software",
    "technology", "hangman", "education", "engineer"
]

# Step 2: ASCII Hangman stages (0 to 6 mistakes)
stages = [
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

# Step 3: Select a random word
secret_word = random.choice(words).upper()

# Step 4: Initialize variables
guessed_letters = set()
wrong_guesses = set()
attempts = 6

print("\n===== WELCOME TO HANGMAN =====")

# Step 5: Main game loop
while attempts > 0:

    # Display current hangman stage
    print(stages[6 - attempts])

    # Display masked word
    display_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("\nWord:", display_word)
    print("Attempts remaining:", attempts)
    print("Guessed letters:", " ".join(sorted(guessed_letters | wrong_guesses)))

    # Check winning condition
    if all(letter in guessed_letters for letter in secret_word):
        print("\nCongratulations! You guessed the word!")
        break

    # Get user input
    guess = input("\nGuess a letter: ").strip().upper()

    # Validate input
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter only one alphabet letter.")
        continue

    # Prevent duplicate guesses
    if guess in guessed_letters or guess in wrong_guesses:
        print("You already guessed that letter!")
        continue

    # Check the guess
    if guess in secret_word:
        guessed_letters.add(guess)
        print("Correct guess!")
    else:
        wrong_guesses.add(guess)
        attempts -= 1
        print("Wrong guess!")

else:
    print(stages[6])
    print("\nGAME OVER!")
    print("The correct word was:", secret_word)

print("\n===== THANK YOU FOR PLAYING =====")
