import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        root.title("Dark/Light Mode Example")
        self.is_dark_mode = False
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Hello, World!", font=("Arial", 24))
        self.label.pack(pady=20)

        self.toggle_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_theme)
        self.toggle_button.pack()

    def toggle_theme(self):
         self.is_dark_mode = not self.is_dark_mode
         self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.root.config(bg="black")
            self.label.config(bg="black", fg="white")
            self.toggle_button.config(bg="grey", fg = "white")
        else:
            self.root.config(bg="white")
            self.label.config(bg="white", fg="black")
            self.toggle_button.config(bg="lightgrey", fg = "black")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()