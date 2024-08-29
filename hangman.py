import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame
from tkinter import ttk 

pygame.mixer.init()
HIGH_SCORES_FILE = "high_scores.txt"

CORRECT_SOUND = 'correct.wav'
WIN_SOUND = 'win.wav'
LOSE_SOUND = 'lose.wav'

def play_sound(sound_file):
    if os.path.exists(sound_file):
        pygame.mixer.Sound(sound_file).play()

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
        return "\n".join(scores[:5])
    else:
        return "No high scores yet."

def choose_category():
    categories = {
        'Animals': ['elephant', 'giraffe', 'dolphin', 'kangaroo', 'alligator', 'penguin', 'rhinoceros'],
        'Fruits': ['apple', 'banana', 'cherry', 'date', 'grape', 'kiwi', 'mango'],
        'Countries': ['brazil', 'canada', 'denmark', 'egypt', 'finland', 'germany', 'india'],
        'Programming Languages': ['python', 'java', 'kotlin', 'javascript', 'ruby', 'swift', 'golang'],
        'Sports': ['soccer', 'cricket', 'basketball', 'tennis', 'badminton', 'rugby', 'hockey']
    }
    return random.choice(categories[random.choice(list(categories.keys()))])

class HangmanGame(tk.Tk):
    def __init__(self, mode):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("600x500")

        self.mode = mode
        self.word = choose_category()
        self.guessed_letters = set()
        self.attempts_remaining = 6
        self.current_player = 1

        self.setup_gui()
        self.update_display()

    def setup_gui(self):
        self.word_display = tk.Label(self, text="", font=("Helvetica", 18))
        self.word_display.pack(pady=20)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.make_guess)

        self.attempts_label = tk.Label(self, text=f"Attempts Remaining: {self.attempts_remaining}")
        self.attempts_label.pack(pady=10)

        self.player_label = tk.Label(self, text=f"Player {self.current_player}'s Turn", font=("Helvetica", 12))
        self.player_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=20)
        
        self.high_scores_label = tk.Label(self, text=f"High Scores:\n{display_high_scores()}", font=("Helvetica", 12))
        self.high_scores_label.pack(pady=20)

        if self.mode == 'multiplayer':
            self.player_label.config(text=f"Player {self.current_player}'s Turn")

    def update_display(self):
        display_word = ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        self.word_display.config(text=display_word)
        self.attempts_label.config(text=f"Attempts Remaining: {self.attempts_remaining}")
        self.update_progress_bar()

    def update_progress_bar(self):
        progress = (self.attempts_remaining / 6) * 100
        self.progress_bar['value'] = progress
        self.progress_bar['maximum'] = 100

    def make_guess(self, event):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                messagebox.showinfo("Hangman", "You've already guessed that letter.")
            else:
                self.guessed_letters.add(guess)
                if guess in self.word:
                    play_sound(CORRECT_SOUND)
                else:
                    self.attempts_remaining -= 1
                self.check_game_status()
                self.update_display()
                if self.mode == 'multiplayer':
                    self.switch_player()
        else:
            messagebox.showwarning("Hangman", "Please enter a single valid letter.")

    def check_game_status(self):
        if all(letter in self.guessed_letters for letter in self.word):
            play_sound(WIN_SOUND)
            messagebox.showinfo("Hangman", f"Congratulations! Player {self.current_player} guessed the word '{self.word}' correctly!")
            self.save_and_reset()
        elif self.attempts_remaining == 0:
            play_sound(LOSE_SOUND)
            messagebox.showinfo("Hangman", f"Game over! The word was '{self.word}'. Better luck next time.")
            self.save_and_reset()

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
        self.player_label.config(text=f"Player {self.current_player}'s Turn")

    def save_and_reset(self):
        score = f"{self.attempts_remaining} attempts left - Word: {self.word} - Player {self.current_player}"
        save_high_score(score)
        self.word = choose_category()
        self.guessed_letters.clear()
        self.attempts_remaining = 6
        self.current_player = 1  
        self.high_scores_label.config(text=f"High Scores:\n{display_high_scores()}")
        self.update_display()

class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Start Menu")
        self.geometry("300x200")

        self.setup_menu()

    def setup_menu(self):
        tk.Label(self, text="Welcome to Hangman!", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(self, text="Single Player", command=self.start_single_player).pack(pady=10)
        tk.Button(self, text="Multiplayer", command=self.start_multiplayer).pack(pady=10)

    def start_single_player(self):
        self.destroy() 
        HangmanGame(mode='single').mainloop()

    def start_multiplayer(self):
        self.destroy() 
        HangmanGame(mode='multiplayer').mainloop()

if __name__ == "__main__":
    StartMenu().mainloop()
