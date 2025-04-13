from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import random

class QuizTakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Taker")

        ttk.Label(root, text="Welcome to Quiz Bowl!").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(root, text="Select Class:").grid(row=1, column=0, padx=10, pady=5)
        self.class_var = StringVar()
        self.class_menu = ttk.Combobox(root, textvariable=self.class_var)
        self.class_menu['values'] = ['ds_3850', 'econ_3610', 'mkt_4100', 'mkt_4900', 'ds_3841']
        self.class_menu.grid(row=1, column=1, padx=10, pady=5)

        self.start_btn = ttk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def start_quiz(self):
        self.table = self.class_var.get()
        if not self.table:
            messagebox.showerror("Error", "Please select a class.")
            return

        all_questions = self.load_questions(self.table)

        if not all_questions:
            messagebox.showinfo("No Questions", "This class has no questions.")
            return

        random.shuffle(all_questions)
        self.questions = all_questions[:10]  # limit to 10 questions

        self.score = 0
        self.index = 0
        self.show_question()

    def load_questions(self, table):
        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM {table}")
            questions = cursor.fetchall()
            conn.close()
            return questions
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.index >= len(self.questions):
            messagebox.showinfo("Quiz Completed", f"Your score: {self.score} / {len(self.questions)}")
            self.root.destroy()
            return

        q = self.questions[self.index]
        self.correct_answer = q[5].strip().upper()

        ttk.Label(self.root, text=f"Question {self.index + 1} of {len(self.questions)}:\n{q[0]}").grid(row=0, column=0, columnspan=2, pady=10)

        self.answer_var = StringVar()

        options = ['A', 'B', 'C', 'D']
        for i, letter in enumerate(options):
            text = f"{letter}. {q[i + 1]}"
            ttk.Radiobutton(self.root, text=text, variable=self.answer_var, value=letter).grid(row=i+1, column=0, columnspan=2, sticky=W, padx=20)

        ttk.Button(self.root, text="Submit Answer", command=self.check_answer).grid(row=6, column=0, columnspan=2, pady=10)

    def check_answer(self):
        answer = self.answer_var.get()
        if not answer:
            messagebox.showerror("Error", "Please select an answer.")
            return

        if answer.upper() == self.correct_answer:
            self.score += 1

        self.index += 1
        self.show_question()


if __name__ == "__main__":
    root = Tk()
    app = QuizTakerApp(root)
    root.mainloop()

