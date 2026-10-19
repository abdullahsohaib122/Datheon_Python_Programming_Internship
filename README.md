# Hangman Game — Python

A simple command-line Hangman game built with Python as part of my Python Programming Internship Task 1.

## Features

- Random word selection using Python's `random.choice()`
- Six attempts to guess the hidden word
- ASCII Hangman drawings that update after incorrect guesses
- Displays correctly guessed letters
- Tracks previously guessed letters
- Prevents duplicate guesses from reducing attempts
- Shows victory and game-over messages

## Technologies Used

- Python
- Random module
- Sets and lists
- Loops and conditional statements

## How to Run

1. Install Python.
2. Download or clone this repository.
3. Open the project folder in a terminal.
4. Run the following command:

```bash
python hangman.py
```

5. Enter one letter at a time to guess the hidden word.

## Testing

The game was tested for:
- Correct letter guesses
- Incorrect guesses and attempt reduction
- Repeated letter guesses
- Winning the game
- Losing after six incorrect guesses
- Random word selection across game sessions

## Author

Abdullah Sohaib