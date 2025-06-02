import tkinter as tk
from tkinter import messagebox

# Create the main window (it can be hidden if you only need the pop-up)
root = tk.Tk()
root.withdraw()  # Hide the main window

# Display different types of message boxes
messagebox.showinfo("Title", "Information message")
messagebox.showwarning("Title", "Warning message")
messagebox.showerror("Title", "Error message")

# Ask a question with Yes/No options
if messagebox.askyesno("Title", "Are you sure?"):
    print("User clicked Yes")
else:
    print("User clicked No")

# Ask a question with OK/Cancel options
if messagebox.askokcancel("Title", "Proceed?"):
    print("User clicked OK")
else:
    print("User clicked Cancel")

# The program will wait for user interaction with the message box
# before continuing or exiting.