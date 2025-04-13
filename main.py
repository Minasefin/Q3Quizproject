from tkinter import *
from tkinter import ttk
import subprocess
import sys

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl Main Menu")
        self.root.geometry("300x200")

        ttk.Label(root, text="Welcome to Quiz Bowl!", font=("Helvetica", 14)).pack(pady=20)

        ttk.Button(root, text="Take Quiz", command=self.launch_quiz).pack(pady=10)
        ttk.Button(root, text="Admin Login", command=self.launch_admin).pack(pady=10)

    def launch_quiz(self):
        subprocess.Popen([sys.executable, "quizTaker.py"])

    def launch_admin(self):
        subprocess.Popen([sys.executable, "adminGUI.py"])


if __name__ == "__main__":
    root = Tk()
    app = MainMenu(root)
    root.mainloop()
