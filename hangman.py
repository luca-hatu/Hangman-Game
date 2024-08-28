import random
import os

HIGH_SCORES_FILE = "high_scores.txt"

def choose_category():
    categories = {
        'Animals': ['elephant', 'giraffe', 'dolphin', 'kangaroo', 'alligator', 'penguin', 'rhinoceros'],
        'Fruits': ['apple', 'banana', 'cherry', 'date', 'grape', 'kiwi', 'mango'],
        'Countries': ['brazil', 'canada', 'denmark', 'egypt', 'finland', 'germany', 'india', 'france'],
        'Programming Languages': ['python', 'java', 'kotlin', 'javascript', 'ruby', 'swift', 'golang'],
        'Sports': ['football', 'cricket', 'basketball', 'tennis', 'badminton', 'rugby', 'hockey']
    }
    
    print("Please choose a category:")
    for i, category in enumerate(categories.keys(), 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(categories):
                chosen_category = list(categories.keys())[choice - 1]
                print(f"You chose: {chosen_category}")
                return random.choice(categories[chosen_category])
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")

def display_game_state(word, guessed_letters):
    display = ''.join([letter if letter in guessed_letters else '_' for letter in word])
    print(f"Word: {display}")

def get_guess(guessed_letters):
    while True:
        guess = input("Guess a letter: ").lower()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You've already guessed that letter.")
            else:
                return guess
        else:
            print("Please enter a single valid letter.")

def draw_hangman(attempts_remaining):
    stages = [
        """
           ------
           |    |
           |
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------
        """
    ]
    print(stages[6 - attempts_remaining])

def load_high_scores():
    if not os.path.exists(HIGH_SCORES_FILE):
        return []

    with open(HIGH_SCORES_FILE, 'r') as file:
        scores = [line.strip() for line in file.readlines()]
    return scores

def save_high_score(new_score):
    scores = load_high_scores()
    scores.append(new_score)
    scores.sort()
    with open(HIGH_SCORES_FILE, 'w') as file:
        for score in scores:
            file.write(f"{score}\n")

def display_high_scores():
    scores = load_high_scores()
    if scores:
        print("\nHigh Scores:")
        for i, score in enumerate(scores[:5], 1):
            print(f"{i}. {score}")
    else:
        print("\nNo high scores yet.")

def play_hangman():
    word = choose_category()
    guessed_letters = set()
    attempts_remaining = 6
    won = False

    print("Welcome to Hangman!")
    print(f"The word has {len(word)} letters.")
    
    display_high_scores()

    while attempts_remaining > 0 and not won:
        draw_hangman(attempts_remaining)
        display_game_state(word, guessed_letters)
        print(f"Attempts remaining: {attempts_remaining}")
        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in word:
            print(f"Good job! The letter '{guess}' is in the word.")
            if all(letter in guessed_letters for letter in word):
                won = True
        else:
            print(f"Sorry, the letter '{guess}' is not in the word.")
            attempts_remaining -= 1

    if won:
        print(f"Congratulations! You've guessed the word '{word}' correctly!")
        score = f"{attempts_remaining} attempts left - Word: {word}"
        save_high_score(score)
    else:
        draw_hangman(0)
        print(f"Game over! The word was '{word}'. Better luck next time.")

if __name__ == "__main__":
    play_hangman()
