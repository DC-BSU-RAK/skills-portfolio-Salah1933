import tkinter as tk
import random

# --------------------------------------
# Read Jokes from File
# --------------------------------------
def load_jokes():
    jokes = []
    with open("randomJokes.txt", "r") as f:
        for line in f:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline))
    return jokes

jokes = load_jokes()

# --------------------------------------
# FUNCTIONS
# --------------------------------------

def show_setup():
    """Display setup of a random joke."""
    global current_joke
    current_joke = random.choice(jokes)
    
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")  # Clear old punchline

def show_punchline():
    """Display punchline of current joke."""
    if current_joke:
        punchline_label.config(text=current_joke[1])

# --------------------------------------
# GUI SETUP
# --------------------------------------

root = tk.Tk()
root.title("Alexa - Tell Me a Joke")
root.geometry("400x300")

current_joke = None

# Setup display labels
setup_label = tk.Label(root, text="", font=("Arial", 14), wraplength=350)
setup_label.pack(pady=20)

punchline_label = tk.Label(root, text="", font=("Arial", 14, "italic"), wraplength=350)
punchline_label.pack(pady=10)

# Buttons
tk.Button(root, text="Alexa Tell Me a Joke", command=show_setup).pack(pady=5)
tk.Button(root, text="Show Punchline", command=show_punchline).pack(pady=5)
tk.Button(root, text="Next Joke", command=show_setup).pack(pady=5)
tk.Button(root, text="Quit", command=root.destroy).pack(pady=5)

root.mainloop()
