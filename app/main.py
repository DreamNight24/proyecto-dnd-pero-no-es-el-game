import tkinter as tk
from gui import Application
from models import Estado

def main():
    Estado.inicializar_estados_base()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
                                                                