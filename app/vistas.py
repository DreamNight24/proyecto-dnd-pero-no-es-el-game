import tkinter as tk
from tkinter import messagebox
from app.crud import crear_usuario, crear_personaje, obtener_personajes

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Infinity Creations - Juego de Rol")
        self.geometry("800x600")
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nombre del jugador (real)").grid(row=0, column=0)
        self.entry_nombre_jugador = tk.Entry(self)
        self.entry_nombre_jugador.grid(row=0, column=1)

        tk.Label(self, text="Nombre del personaje").grid(row=1, column=0)
        self.entry_nombre_personaje = tk.Entry(self)
        self.entry_nombre_personaje.grid(row=1, column=1)

        tk.Label(self, text="Raza").grid(row=2, column=0)
        self.entry_raza = tk.Entry(self)
        self.entry_raza.grid(row=2, column=1)

        tk.Label(self, text="Estado").grid(row=3, column=0)
        self.entry_estado = tk.Entry(self)
        self.entry_estado.grid(row=3, column=1)

        tk.Button(self, text="Guardar Personaje", command=self.guardar_personaje).grid(row=4, column=1)
        tk.Button(self, text="Ver Personajes", command=self.ver_personajes).grid(row=5, column=1)

    def guardar_personaje(self):
        nombre_jugador = self.entry_nombre_jugador.get()
        nombre_personaje = self.entry_nombre_personaje.get()
        raza = self.entry_raza.get()
        estado = self.entry_estado.get()

        # Aquí deberías añadir lógica para obtener el id_usuario, id_raza y id_estado desde la base de datos.
        # Por simplicidad, usamos valores hardcodeados.
        id_usuario = 1
        id_raza = 1
        id_estado = 1

        crear_personaje(id_usuario, nombre_personaje, id_raza, id_estado)
        messagebox.showinfo("Éxito", "Personaje guardado exitosamente")

    def ver_personajes(self):
        personajes = obtener_personajes()
        for personaje in personajes:
            print(personaje.nombre_personaje, personaje.id_raza, personaje.nivel, personaje.id_estado)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
