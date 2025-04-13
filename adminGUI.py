from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Example password
ADMIN_PASSWORD = "admin123"

class AddQuestionForm:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Add Question")

        ttk.Label(self.window, text="Select Class:").grid(row=0, column=0, padx=5, pady=5)
        self.class_var = StringVar()
        self.class_menu = ttk.Combobox(self.window, textvariable=self.class_var)
        self.class_menu['values'] = ['ds_3850', 'econ_3610', 'mkt_4100', 'mkt_4900', 'ds_3841']
        self.class_menu.grid(row=0, column=1, padx=5, pady=5)

        self.entries = {}
        labels = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        for i, label in enumerate(labels, start=1):
            ttk.Label(self.window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.window, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        self.submit_btn = ttk.Button(self.window, text="Submit", command=self.submit_question)
        self.submit_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    def submit_question(self):
        table = self.class_var.get()
        data = [self.entries[label].get().strip() for label in self.entries]

        if not table or any(not val for val in data):
            messagebox.showerror("Error", "Please fill out all fields and select a class.")
            return

        question, a, b, c, d, correct = data

        if correct.upper() not in ['A', 'B', 'C', 'D']:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.")
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO {table} (question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (question, a, b, c, d, correct.upper()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Question added successfully!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


class EditQuestionPopup:
    def __init__(self, table, question_id, refresh_callback):
        self.table = table
        self.qid = question_id
        self.refresh = refresh_callback

        self.window = Toplevel()
        self.window.title("Edit Question")

        self.labels = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            ttk.Label(self.window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.window, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        self.submit_btn = ttk.Button(self.window, text="Update", command=self.update_question)
        self.submit_btn.grid(row=len(self.labels), column=0, columnspan=2, pady=10)

        self.load_question()

    def load_question(self):
        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT question, option_a, option_b, option_c, option_d, correct_answer
                FROM {self.table} WHERE id = ?
            ''', (self.qid,))
            result = cursor.fetchone()
            conn.close()

            for i, key in enumerate(self.labels):
                self.entries[key].insert(0, result[i])
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_question(self):
        data = [self.entries[label].get().strip() for label in self.labels]

        if any(not val for val in data):
            messagebox.showerror("Error", "All fields are required.")
            return

        question, a, b, c, d, correct = data

        if correct.upper() not in ['A', 'B', 'C', 'D']:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.")
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE {self.table}
                SET question=?, option_a=?, option_b=?, option_c=?, option_d=?, correct_answer=?
                WHERE id=?
            ''', (question, a, b, c, d, correct.upper(), self.qid))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Question updated successfully.")
            self.window.destroy()
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


class ViewEditDeleteForm:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("View/Edit/Delete Questions")

        ttk.Label(self.window, text="Select Class:").grid(row=0, column=0, padx=5, pady=5)
        self.class_var = StringVar()
        self.class_menu = ttk.Combobox(self.window, textvariable=self.class_var)
        self.class_menu['values'] = ['ds_3850', 'econ_3610', 'mkt_4100', 'mkt_4900', 'ds_3841']
        self.class_menu.grid(row=0, column=1, padx=5, pady=5)

        self.load_btn = ttk.Button(self.window, text="Load Questions", command=self.load_questions)
        self.load_btn.grid(row=0, column=2, padx=5, pady=5)

        self.tree = ttk.Treeview(self.window, columns=("ID", "Question", "Answer"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Question", text="Question")
        self.tree.heading("Answer", text="Correct Answer")
        self.tree.column("ID", width=40)
        self.tree.column("Question", width=400)
        self.tree.column("Answer", width=100)
        self.tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.edit_btn = ttk.Button(self.window, text="Edit", command=self.edit_question)
        self.edit_btn.grid(row=2, column=0, pady=10)

        self.delete_btn = ttk.Button(self.window, text="Delete", command=self.delete_question)
        self.delete_btn.grid(row=2, column=1, pady=10)

    def load_questions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        table = self.class_var.get()
        if not table:
            messagebox.showerror("Error", "Please select a class.")
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, question, correct_answer FROM {table}")
            for row in cursor.fetchall():
                self.tree.insert("", END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_question(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a question to delete.")
            return

        table = self.class_var.get()
        item = self.tree.item(selected_item)
        question_id = item["values"][0]

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id = ?", (question_id,))
            conn.commit()
            conn.close()
            self.tree.delete(selected_item)
            messagebox.showinfo("Deleted", "Question deleted successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def edit_question(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a question to edit.")
            return

        table = self.class_var.get()
        item = self.tree.item(selected_item)
        question_id = item["values"][0]

        EditQuestionPopup(table, question_id, self.load_questions)


class AdminLogin:
    def __init__(self, master):
        self.master = master
        master.title("Admin Login")

        self.label = ttk.Label(master, text="Enter Admin Password:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(master, show="*")
        self.password_entry.grid(row=0, column=1, padx=10, pady=10)

        self.login_button = ttk.Button(master, text="Login", command=self.check_password)
        self.login_button.grid(row=1, column=0, columnspan=2, pady=10)

    def check_password(self):
        if self.password_entry.get() == ADMIN_PASSWORD:
            self.master.destroy()
            open_admin_dashboard()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")


class AdminDashboard:
    def __init__(self, master):
        self.master = master
        master.title("Admin Dashboard")

        ttk.Label(master, text="Admin Tools").grid(row=0, column=0, columnspan=2, pady=10)

        self.add_btn = ttk.Button(master, text="Add Questions", command=self.add_question)
        self.add_btn.grid(row=1, column=0, padx=10, pady=5)

        self.view_btn = ttk.Button(master, text="View/Edit/Delete Questions", command=self.view_questions)
        self.view_btn.grid(row=1, column=1, padx=10, pady=5)

        self.exit_btn = ttk.Button(master, text="Exit", command=master.destroy)
        self.exit_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def add_question(self):
        AddQuestionForm()

    def view_questions(self):
        ViewEditDeleteForm()


def open_admin_dashboard():
    dashboard_root = Tk()
    app = AdminDashboard(dashboard_root)
    dashboard_root.mainloop()


if __name__ == '__main__':
    root = Tk()
    login_app = AdminLogin(root)
    root.mainloop()
