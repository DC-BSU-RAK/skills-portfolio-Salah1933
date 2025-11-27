import tkinter as tk
from tkinter import messagebox, ttk


# =======================================================
# Load Student Data
# =======================================================

def load_students():
    students = []
    try:
        with open("Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt", "r") as f:
            count = int(f.readline().strip())
            for _ in range(count):
                line = f.readline().strip().split(",")
                sid = line[0]
                name = line[1]
                c1, c2, c3 = map(int, line[2:5])
                exam = int(line[5])

                coursework_total = c1 + c2 + c3     # out of 60
                overall = coursework_total + exam   # out of 160
                percent = (overall / 160) * 100

                # Grade calculation
                if percent >= 70:
                    grade = "A"
                elif percent >= 60:
                    grade = "B"
                elif percent >= 50:
                    grade = "C"
                elif percent >= 40:
                    grade = "D"
                else:
                    grade = "F"

                students.append({
                    "id": sid,
                    "name": name,
                    "cwork": coursework_total,
                    "exam": exam,
                    "overall": overall,
                    "percent": percent,
                    "grade": grade
                })
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt file not found!")

    return students


students = load_students()


# =======================================================
# Helper function to clear the window
# =======================================================

def clear():
    for widget in frame.winfo_children():
        widget.destroy()


# =======================================================
# Display a single student record in a readable format
# =======================================================

def display_record(stu):
    lines = [
        f"Student Name: {stu['name']}",
        f"Student Number: {stu['id']}",
        f"Coursework Total: {stu['cwork']} / 60",
        f"Exam Mark: {stu['exam']} / 100",
        f"Overall %: {stu['percent']:.2f}%",
        f"Grade: {stu['grade']}"
    ]
    return "\n".join(lines)


# =======================================================
# MENU FUNCTIONALITY
# =======================================================

def view_all():
    clear()
    text = tk.Text(frame, width=60, height=25)
    text.pack()

    total_percent = 0

    for stu in students:
        rec = display_record(stu)
        text.insert(tk.END, rec + "\n" + "-"*40 + "\n")
        total_percent += stu['percent']

    avg = total_percent / len(students)
    summary = f"\nTotal Students: {len(students)}\nAverage Percentage: {avg:.2f}%"
    text.insert(tk.END, summary)


def view_individual():
    clear()
    tk.Label(frame, text="Enter Student Number:", font=("Arial", 12)).pack()

    entry = tk.Entry(frame)
    entry.pack(pady=5)

    def search():
        sid = entry.get()
        for stu in students:
            if stu["id"] == sid:
                messagebox.showinfo("Student Record", display_record(stu))
                return
        messagebox.showerror("Not Found", "Student ID not found.")

    tk.Button(frame, text="Search", command=search).pack(pady=5)


def show_highest():
    clear()
    best = max(students, key=lambda s: s["overall"])
    messagebox.showinfo("Highest Mark", display_record(best))


def show_lowest():
    clear()
    worst = min(students, key=lambda s: s["overall"])
    messagebox.showinfo("Lowest Mark", display_record(worst))


# =======================================================
# MAIN GUI WINDOW
# =======================================================

root = tk.Tk()
root.title("Student Manager")
root.geometry("650x500")

# Left menu
menu_frame = tk.Frame(root, width=200, height=500, bg="#dddddd")
menu_frame.pack(side="left", fill="y")

# Right content frame
frame = tk.Frame(root, width=450, height=500)
frame.pack(side="right", fill="both", expand=True)

# Menu buttons
tk.Label(menu_frame, text="Menu", bg="#dddddd", font=("Arial", 16)).pack(pady=20)

tk.Button(menu_frame, text="1. View All Records", width=20, command=view_all).pack(pady=5)
tk.Button(menu_frame, text="2. View Individual Record", width=20, command=view_individual).pack(pady=5)
tk.Button(menu_frame, text="3. Show Highest Score", width=20, command=show_highest).pack(pady=5)
tk.Button(menu_frame, text="4. Show Lowest Score", width=20, command=show_lowest).pack(pady=5)
tk.Button(menu_frame, text="Quit", width=20, command=root.destroy).pack(pady=20)

root.mainloop() 