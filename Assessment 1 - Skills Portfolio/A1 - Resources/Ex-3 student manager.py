import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

FILENAME = "studentMarks.txt"

# -------------------------------------------------------
# Utility Functions
# -------------------------------------------------------
def load_students():
    students = []
    try:
        with open(FILENAME, "r") as f:
            lines = f.read().strip().split("\n")
            for line in lines[1:]:
                parts = line.split(",")
                s = {
                    "number": int(parts[0]),
                    "name": parts[1],
                    "c1": int(parts[2]),
                    "c2": int(parts[3]),
                    "c3": int(parts[4]),
                    "exam": int(parts[5])
                }
                students.append(s)
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found.")
    return students


def save_students(students):
    with open(FILENAME, "w") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            line = f"{s['number']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
            f.write(line)


def calculate_total(s):
    return s["c1"] + s["c2"] + s["c3"] + s["exam"]


def calculate_percentage(s):
    total = calculate_total(s)
    return (total / 160) * 100


def calculate_grade(percent):
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    else:
        return "F"


# -------------------------------------------------------
# GUI Application
# -------------------------------------------------------
class StudentApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Manager")

        self.students = load_students()

        # Menu Bar
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu)

        menu.add_command(label="1. View All Students", command=self.view_all)
        menu.add_command(label="2. View Individual Student", command=self.view_individual)
        menu.add_command(label="3. Show Highest Score", command=self.highest_score)
        menu.add_command(label="4. Show Lowest Score", command=self.lowest_score)
        menu.add_separator()
        menu.add_command(label="5. Sort Student Records", command=self.sort_students)
        menu.add_command(label="6. Add Student Record", command=self.add_student)
        menu.add_command(label="7. Delete Student Record", command=self.delete_student)
        menu.add_command(label="8. Update Student Record", command=self.update_student)

        # Output box
        self.output = tk.Text(master, width=80, height=25, font=("Arial", 12))
        self.output.pack(pady=10)

    # -------------------------------------------------------
    # Output Helper
    # -------------------------------------------------------
    def display_student(self, s):
        total = calculate_total(s)
        percent = calculate_percentage(s)
        grade = calculate_grade(percent)

        self.output.insert(tk.END, f"Name: {s['name']}\n")
        self.output.insert(tk.END, f"Student Number: {s['number']}\n")
        self.output.insert(tk.END, f"Coursework Total: {s['c1'] + s['c2'] + s['c3']}\n")
        self.output.insert(tk.END, f"Exam Mark: {s['exam']}\n")
        self.output.insert(tk.END, f"Overall %: {percent:.1f}%\n")
        self.output.insert(tk.END, f"Grade: {grade}\n")
        self.output.insert(tk.END, "-" * 40 + "\n")

    # -------------------------------------------------------
    # 1. View all student records
    # -------------------------------------------------------
    def view_all(self):
        self.output.delete("1.0", tk.END)
        total_percent = 0

        for s in self.students:
            self.display_student(s)
            total_percent += calculate_percentage(s)

        avg = total_percent / len(self.students)
        self.output.insert(tk.END, f"\nTotal students: {len(self.students)}\n")
        self.output.insert(tk.END, f"Average percentage: {avg:.1f}%\n")

    # -------------------------------------------------------
    # 2. View individual record
    # -------------------------------------------------------
    def view_individual(self):
        target = simpledialog.askstring("Search", "Enter student name or number:")

        if target is None:
            return

        for s in self.students:
            if target.lower() == s["name"].lower() or target == str(s["number"]):
                self.output.delete("1.0", tk.END)
                self.display_student(s)
                return

        messagebox.showinfo("Not Found", "Student not found.")

    # -------------------------------------------------------
    # 3. Highest score
    # -------------------------------------------------------
    def highest_score(self):
        self.output.delete("1.0", tk.END)
        best = max(self.students, key=lambda s: calculate_total(s))
        self.display_student(best)

    # -------------------------------------------------------
    # 4. Lowest score
    # -------------------------------------------------------
    def lowest_score(self):
        self.output.delete("1.0", tk.END)
        worst = min(self.students, key=lambda s: calculate_total(s))
        self.display_student(worst)

    # -------------------------------------------------------
    # 5. Sort records
    # -------------------------------------------------------
    def sort_students(self):
        method = simpledialog.askstring("Sort", "Sort by name or number? (name/number)")
        order = simpledialog.askstring("Sort", "Ascending or descending? (a/d)")

        reverse = (order.lower() == "d")

        if method == "name":
            self.students.sort(key=lambda s: s["name"].lower(), reverse=reverse)
        else:
            self.students.sort(key=lambda s: s["number"], reverse=reverse)

        self.view_all()

    # -------------------------------------------------------
    # 6. Add a student
    # -------------------------------------------------------
    def add_student(self):
        try:
            number = int(simpledialog.askstring("Add", "Student number:"))
            name = simpledialog.askstring("Add", "Name:")
            c1 = int(simpledialog.askstring("Add", "Coursework 1 (0–20):"))
            c2 = int(simpledialog.askstring("Add", "Coursework 2 (0–20):"))
            c3 = int(simpledialog.askstring("Add", "Coursework 3 (0–20):"))
            exam = int(simpledialog.askstring("Add", "Exam (0–100):"))
        except:
            messagebox.showerror("Error", "Invalid input.")
            return

        new = {"number": number, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam}
        self.students.append(new)
        save_students(self.students)
        messagebox.showinfo("Success", "Student added.")

    # -------------------------------------------------------
    # 7. Delete a student
    # -------------------------------------------------------
    def delete_student(self):
        target = simpledialog.askstring("Delete", "Enter student name or number:")

        for s in self.students:
            if target.lower() == s["name"].lower() or target == str(s["number"]):
                self.students.remove(s)
                save_students(self.students)
                messagebox.showinfo("Deleted", "Student removed.")
                return

        messagebox.showinfo("Not Found", "Student not found.")

    # -------------------------------------------------------
    # 8. Update a student
    # -------------------------------------------------------
    def update_student(self):
        target = simpledialog.askstring("Update", "Enter student name or number:")

        for s in self.students:
            if target.lower() == s["name"].lower() or target == str(s["number"]):

                field = simpledialog.askstring(
                    "Update",
                    "What to update? (name, number, c1, c2, c3, exam)"
                )

                if field not in s:
                    messagebox.showerror("Error", "Invalid field.")
                    return

                new_value = simpledialog.askstring("Update", "Enter new value:")

                if field in ["number", "c1", "c2", "c3", "exam"]:
                    new_value = int(new_value)

                s[field] = new_value
                save_students(self.students)

                messagebox.showinfo("Success", "Record updated.")
                return

        messagebox.showinfo("Not Found", "Student not found.")


# -------------------------------------------------------
# Run Application
# -------------------------------------------------------
root = tk.Tk()
app = StudentApp(root)
root.mainloop()
