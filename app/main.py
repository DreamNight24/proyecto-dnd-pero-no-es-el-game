import tkinter as tk
from gui import Application

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
