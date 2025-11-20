import tkinter as tk
from tkinter import messagebox
import random

# ----------------------
# FUNCTIONS
# ----------------------

def displayMenu():
    """Show difficulty menu."""
    clearWindow()
    tk.Label(root, text="DIFFICULTY LEVEL", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="1. Easy", width=20, command=lambda: startQuiz(1)).pack(pady=5)
    tk.Button(root, text="2. Moderate", width=20, command=lambda: startQuiz(2)).pack(pady=5)
    tk.Button(root, text="3. Advanced", width=20, command=lambda: startQuiz(3)).pack(pady=5)

def randomInt(level):
    """Return number based on difficulty."""
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

def decideOperation():
    """Randomly choose + or -"""
    return random.choice(["+", "-"])

def displayProblem():
    """Show current arithmetic problem."""
    global num1, num2, op

    clearWindow()

    tk.Label(root, text=f"Question {questionNumber} of 10",
             font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text=f"{num1} {op} {num2} = ",
             font=("Arial", 20)).pack(pady=10)

    answerEntry.pack(pady=10)
    answerEntry.delete(0, tk.END)

    tk.Button(root, text="Submit", command=checkAnswer).pack(pady=10)

def isCorrect(userAns):
    """Check if user's answer is correct."""
    if op == "+":
        return userAns == num1 + num2
    else:
        return userAns == num1 - num2

def checkAnswer():
    global score, attempts, questionNumber
    try:
        userAns = int(answerEntry.get())
    except:
        messagebox.showwarning("Error", "Please enter a number!")
        return

    if isCorrect(userAns):
        if attempts == 1:
            score += 10
        else:
            score += 5
        messagebox.showinfo("Correct", "Correct!")
        nextQuestion()
    else:
        if attempts == 1:
            attempts = 2
            messagebox.showwarning("Try Again", "Incorrect. Try once more!")
            displayProblem()
        else:
            messagebox.showinfo("Incorrect", "Wrong again! Moving on.")
            nextQuestion()

def nextQuestion():
    """Load next question or finish quiz."""
    global questionNumber, num1, num2, op, attempts

    questionNumber += 1
    attempts = 1

    if questionNumber > 10:
        displayResults()
        return

    num1 = randomInt(level)
    num2 = randomInt(level)
    op = decideOperation()

    displayProblem()

def displayResults():
    """Show final score & grade."""
    clearWindow()
    tk.Label(root, text=f"Your final score: {score}/100",
             font=("Arial", 18)).pack(pady=10)

    # grade
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"

    tk.Label(root, text=f"Grade: {grade}", font=("Arial", 18)).pack(pady=10)

    tk.Button(root, text="Play Again", command=displayMenu).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

def startQuiz(chosenLevel):
    """Initialize quiz variables."""
    global level, questionNumber, score, attempts, num1, num2, op

    level = chosenLevel
    questionNumber = 1
    score = 0
    attempts = 1

    num1 = randomInt(level)
    num2 = randomInt(level)
    op = decideOperation()

    displayProblem()

def clearWindow():
    """Remove all widgets."""
    for widget in root.winfo_children():
        widget.destroy()

# ----------------------
# MAIN WINDOW
# ----------------------

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("350x300")

answerEntry = tk.Entry(root, font=("Arial", 18))

displayMenu()

root.mainloop()
