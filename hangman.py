import random

def choose_word():
    words = ['python', 'java', 'hackclub', 'javascript', 'hangman', 'hakkun', 'arcade']
    return random.choice(words)

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
           |    O
           |   /|\\
           |   / \\
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
           |    |
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
           |    
           |    
           |    
           |
        --------
        """
    ]
    print(stages[6 - attempts_remaining])

def play_hangman():
    word = choose_word()
    guessed_letters = set()
    attempts_remaining = 6
    won = False

    print("Welcome to Hangman!")
    print(f"The word has {len(word)} letters.")

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
    else:
        draw_hangman(0)
        print(f"Game over! The word was '{word}'. Better luck next time.")

if __name__ == "__main__":
    play_hangman()
