import tkinter as tk


def apply_theme(theme):
    if theme == "dark":
        bg = "#333"
        fg = "white"
        entry_bg = "#555"
        button_bg = "#444"
    else:  # light mode
        bg = "white"
        fg = "black"
        entry_bg = "white"
        button_bg = "lightgray"

    window.config(bg=bg)
    for widget in window.winfo_children():
        widget.config(bg=bg, fg=fg)
        if isinstance(widget, tk.Entry):
            widget.config(bg=entry_bg, fg=fg)
        if isinstance(widget, tk.Button):
            widget.config(bg=button_bg, fg=fg)


def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(current_theme)


window = tk.Tk()
current_theme = "light"

# Example widgets
tk.Label(window, text="Sample Text").pack(pady=10)
tk.Entry(window).pack(pady=5)
tk.Button(window, text="Change Theme", command=toggle_theme).pack(pady=10)

apply_theme(current_theme)
window.mainloop()
