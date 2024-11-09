import tkinter as tk
from tkinter import messagebox
import random
import time

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("600x500")
        
        # Set a colorful background color
        self.root.configure(bg="#282c34")

        self.easy_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "A journey of a thousand miles begins with a single step."
        ]
        self.medium_texts = [
            "Long ago, before the Moonlit Garden came to be, there was a little girl named Lily",
            "Lily spent hours exploring the garden, marveling at its wonders. She met friendly fairies who showed her their homes and played"
        ]
        self.hard_texts = [
            "Once upon a time, in a small village nestled between rolling hills and lush forests, there was a magical garden. This garden was unlike any other, for it only came to life under the gentle glow of the moon.",
            "In this garden lived a variety of enchanting creatures—fairies with shimmering wings, talking animals, and flowers that danced to the melody of the night breeze. But the most remarkable of all was a wise old owl named Oliver."
            "At the bottom, she found herself in a magnificent underground garden, illuminated by glowing crystals embedded in the walls. It was the most beautiful place she had ever seen. Flowers of every color bloomed all around, and the air was filled with the sweet scent of jasmine and honeysuckle."
        ]

        # Add title label
        self.title_label = tk.Label(root, text="Typing Speed Test", font=("Helvetica", 20, "bold"), fg="white", bg="#282c34")
        self.title_label.pack(pady=10)

        # Create a frame to hold the content
        self.frame = tk.Frame(root, bg="#61dafb", bd=5)
        self.frame.place(relx=0.5, rely=0.2, relwidth=0.85, relheight=0.6, anchor='n')

        self.label = tk.Label(self.frame, text="Select difficulty and type the text as fast as you can:", font=("Helvetica", 14), bg="#61dafb")
        self.label.pack(pady=10)

        self.difficulty_var = tk.StringVar(value="easy")
        self.easy_button = tk.Radiobutton(self.frame, text="Easy", variable=self.difficulty_var, value="easy", command=self.select_text, bg="#98FB98", font=("Helvetica", 12))
        self.easy_button.pack(pady=5)
        self.medium_button = tk.Radiobutton(self.frame, text="Medium", variable=self.difficulty_var, value="medium", command=self.select_text, bg="#FFD700", font=("Helvetica", 12))
        self.medium_button.pack(pady=5)
        self.hard_button = tk.Radiobutton(self.frame, text="Hard", variable=self.difficulty_var, value="hard", command=self.select_text, bg="#FF6347", font=("Helvetica", 12))
        self.hard_button.pack(pady=5)

        self.text_label = tk.Label(self.frame, wraplength=400, font=("Helvetica", 12), bg="#ffffff", borderwidth=2, relief="groove")
        self.text_label.pack(pady=10)

        self.entry = tk.Entry(self.frame, width=50, font=("Helvetica", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.check_completion)

        self.start_button = tk.Button(self.frame, text="Start", command=self.start_test, bg="#32CD32", font=("Helvetica", 12), width=10)
        self.start_button.pack(pady=5)

        self.finish_button = tk.Button(self.frame, text="Finish", command=self.finish_test, bg="#ff6666", font=("Helvetica", 12), width=10, state=tk.DISABLED)
        self.finish_button.pack(pady=5)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset_test, bg="#ffcc66", font=("Helvetica", 12), width=10)
        self.reset_button.pack(pady=5)

        self.leaderboard_button = tk.Button(self.frame, text="Leaderboard", command=self.show_leaderboard, bg="#00BFFF", font=("Helvetica", 12), width=10)
        self.leaderboard_button.pack(pady=5)

        self.pause_button = tk.Button(self.frame, text="Pause", command=self.pause_test, bg="#D3D3D3", font=("Helvetica", 12), width=10)
        self.pause_button.pack(pady=5)

        self.resume_button = tk.Button(self.frame, text="Resume", command=self.resume_test, bg="#32CD32", font=("Helvetica", 12), width=10, state=tk.DISABLED)
        self.resume_button.pack(pady=5)

        self.start_time = None
        self.pause_time = None
        self.selected_text = ""
        self.leaderboard = []

    def select_text(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "easy":
            self.selected_text = random.choice(self.easy_texts)
        elif difficulty == "medium":
            self.selected_text = random.choice(self.medium_texts)
        else:
            self.selected_text = random.choice(self.hard_texts)
        self.text_label.config(text=self.selected_text)

    def start_test(self):
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.finish_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)

    def finish_test(self):
        if self.start_time is None:
            messagebox.showwarning("Warning", "You need to start the test first!")
        else:
            self.calculate_speed()
            self.start_button.config(state=tk.NORMAL)
            self.finish_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)

    def check_completion(self, event):
        typed_text = self.entry.get()
        if typed_text == self.selected_text:
            self.finish_test()

    def calculate_speed(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        typed_text = self.entry.get()
        words_typed = len(typed_text.split())
        words_per_minute = (words_typed / elapsed_time) * 60

        correct_characters = sum(1 for expected, typed in zip(self.selected_text, typed_text) if expected == typed)
        accuracy = (correct_characters / len(self.selected_text)) * 100

        messagebox.showinfo("Results", f"Time taken: {elapsed_time:.2f} seconds\n"
                                       f"Words typed: {words_typed}\n"
                                       f"Typing speed: {words_per_minute:.2f} WPM\n"
                                       f"Accuracy: {accuracy:.2f}%")

        # Add result to leaderboard
        self.leaderboard.append((words_per_minute, accuracy))
        self.leaderboard.sort(reverse=True, key=lambda x: x[0])

    def reset_test(self):
        self.select_text()
        self.entry.delete(0, tk.END)
        self.start_time = None
        self.start_button.config(state=tk.NORMAL)
        self.finish_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)

    def show_leaderboard(self):
        leaderboard_text = "Leaderboard:\n"
        for i, (wpm, accuracy) in enumerate(self.leaderboard[:10], 1):
            leaderboard_text += f"{i}. {wpm:.2f} WPM - {accuracy:.2f}% accuracy\n"
        messagebox.showinfo("Leaderboard", leaderboard_text)

    def pause_test(self):
        if self.start_time:
            self.pause_time = time.time()
            self.entry.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_test(self):
        if self.pause_time:
            pause_duration = time.time() - self.pause_time
            self.start_time += pause_duration
            self.entry.config(state=tk.NORMAL)
            self.entry.focus()
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    app.select_text()  # Initialize with a text
    root.mainloop()
