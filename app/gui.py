import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import Usuario, Personaje, Raza, Estado, Habilidad, Poder, Equipamiento, Personaje_Equipamiento

class Application(tk.Frame): 
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Juego de Rol")
        self.pack()
        self.usuario_actual = None
        self.create_widgets()

    def create_widgets(self):
        self.login_button = ttk.Button(self, text="Iniciar Sesión", command=self.login)
        self.login_button.pack()

        self.register_button = ttk.Button(self, text="Registrarse", command=self.register)
        self.register_button.pack()

    def login(self):
        LoginWindow(self.master, self.on_login_success)

    def register(self):
        RegisterWindow(self.master)

    def on_login_success(self, usuario):
        self.usuario_actual = usuario
        if usuario.es_gm:
            GMInterface(self.master, usuario)
        else:
            JugadorInterface(self.master, usuario)

class LoginWindow(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.title("Iniciar Sesión")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.usuario_entry = ttk.Entry(self)
        self.usuario_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Contraseña:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.contrasena_entry = ttk.Entry(self, show="*")
        self.contrasena_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self, text="Iniciar Sesión", command=self.verificar_login).grid(row=2, column=0, columnspan=2, pady=10)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        usuario_obj = Usuario.verificar_credenciales(usuario, contrasena)
        if usuario_obj:
            self.callback(usuario_obj)  # Llama al callback con el usuario
            self.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registrarse")
        self.es_gm_var = tk.BooleanVar()  # Variable de control para el Checkbutton
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Usuario:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.usuario_entry = ttk.Entry(self)
        self.usuario_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.contrasena_entry = ttk.Entry(self, show="*")
        self.contrasena_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Checkbutton(self, text="¿Eres GM?", variable=self.es_gm_var).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(self, text="Registrarse", command=self.registrar).grid(row=4, column=0, columnspan=2, pady=10)

    def registrar(self):
        nombre = self.nombre_entry.get()
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        es_gm = self.es_gm_var.get()  # Obtener el valor del checkbox

        if not nombre or not usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        nuevo_usuario = Usuario(Nombre=nombre, Usuario=usuario, Contrasena=contrasena, Es_GM=es_gm)
        nuevo_usuario.save()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.destroy()



class GMInterface(tk.Toplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.usuario = usuario
        self.title("Interfaz de Game Master")
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self, text="Modificar Personajes", command=self.modificar_personajes).pack(pady=5)
        ttk.Button(self, text="Gestionar Habilidades", command=self.gestionar_habilidades).pack(pady=5)
        ttk.Button(self, text="Gestionar Poderes", command=self.gestionar_poderes).pack(pady=5)
        ttk.Button(self, text="Gestionar Razas", command=self.gestionar_razas).pack(pady=5)
        ttk.Button(self, text="Gestionar Equipamiento", command=self.gestionar_equipamiento).pack(pady=5)
        ttk.Button(self, text="Gestionar Estados", command=self.gestionar_estados).pack(pady=5)

    def modificar_personajes(self):
        GMModificadorPersonaje(self)

    def gestionar_habilidades(self):
        GestionHabilidades(self)

    def gestionar_poderes(self):
        GestionPoderes(self)

    def gestionar_razas(self):
        GestionRazasGM(self)

    def gestionar_equipamiento(self):
        GestionEquipamiento(self)

    def gestionar_estados(self):
        GestionEstados(self)


class JugadorInterface(tk.Toplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.usuario = usuario
        self.title(f"Interfaz de Jugador - {usuario.Nombre}")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.crear_personaje_frame = ttk.Frame(self.notebook)
        self.ver_personajes_frame = ttk.Frame(self.notebook)
        self.modificar_equipamiento_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.crear_personaje_frame, text="Crear Personaje")
        self.notebook.add(self.ver_personajes_frame, text="Mis Personajes")
        self.notebook.add(self.modificar_equipamiento_frame, text="Equipamiento")

        self.crear_widgets_crear_personaje()
        self.crear_widgets_ver_personajes()
        self.crear_widgets_modificar_equipamiento()

    def crear_widgets_crear_personaje(self):
        ttk.Button(self.crear_personaje_frame, text="Crear Nuevo Personaje", command=self.abrir_creador_personaje).pack(pady=20)

    def crear_widgets_ver_personajes(self):
        self.personajes_listbox = tk.Listbox(self.ver_personajes_frame, width=50)
        self.personajes_listbox.pack(pady=10)
        self.cargar_personajes()
        ttk.Button(self.ver_personajes_frame, text="Ver Detalles", command=self.ver_detalles_personaje).pack()

    def crear_widgets_modificar_equipamiento(self):
        ttk.Label(self.modificar_equipamiento_frame, text="Selecciona un personaje:").pack(pady=5)
        self.personajes_equipamiento_combobox = ttk.Combobox(self.modificar_equipamiento_frame, state="readonly")
        self.personajes_equipamiento_combobox.pack(pady=5)
        self.cargar_personajes_equipamiento()
        ttk.Button(self.modificar_equipamiento_frame, text="Modificar Equipamiento", command=self.modificar_equipamiento_personaje).pack(pady=10)

    def abrir_creador_personaje(self):
        CreadorPersonaje(self, self.usuario)

    def cargar_personajes(self):
        self.personajes_listbox.delete(0, tk.END)
        personajes = Personaje.get_by_usuario(self.usuario.ID_Usuario)
        for personaje in personajes:
            self.personajes_listbox.insert(tk.END, personaje.Nombre_Personaje)

    def ver_detalles_personaje(self):
        seleccion = self.personajes_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            personaje = Personaje.get_by_usuario(self.usuario.ID_Usuario)[index]
            DetallesPersonaje(self, personaje)

    def cargar_personajes_equipamiento(self):
        personajes = Personaje.get_by_usuario(self.usuario.ID_Usuario)
        self.personajes_equipamiento_combobox['values'] = [p.Nombre_Personaje for p in personajes]
        if personajes:
            self.personajes_equipamiento_combobox.set(personajes[0].Nombre_Personaje)

    def modificar_equipamiento_personaje(self):
        personaje_nombre = self.personajes_equipamiento_combobox.get()
        if personaje_nombre:
            personaje = next((p for p in Personaje.get_by_usuario(self.usuario.ID_Usuario) if p.Nombre_Personaje == personaje_nombre), None)
            if personaje:
                if personaje.ID_Estado == 2:  # Asumiendo que 2 es el ID del estado "Muerto"
                    messagebox.showerror("Error", "No se puede modificar el equipamiento de un personaje muerto")
                    return

                ventana_equipamiento = tk.Toplevel(self)
                ventana_equipamiento.title(f"Modificar Equipamiento de {personaje.Nombre_Personaje}")
                ventana_equipamiento.geometry("400x400")

                frame = ttk.Frame(ventana_equipamiento, padding="10")
                frame.pack(fill=tk.BOTH, expand=True)

                ttk.Label(frame, text="Equipamiento actual:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
                equipamiento_listbox = tk.Listbox(frame, width=50, height=5)
                equipamiento_listbox.grid(row=1, column=0, columnspan=2, pady=(0, 10))

                def cargar_equipamiento():
                    equipamiento_listbox.delete(0, tk.END)
                    for i, equipo in enumerate(personaje.equipamiento):
                        equipamiento_listbox.insert(tk.END, equipo.Nombre_Equipamiento)
                        if i == 0:  # Deshabilitar la selección del primer elemento
                            equipamiento_listbox.itemconfig(i, {'bg': 'light gray'})
                        else:
                            equipamiento_listbox.itemconfig(i, {'bg': 'white'})

                cargar_equipamiento()
                
                def eliminar_equipamiento():
                    seleccion = equipamiento_listbox.curselection()
                    if seleccion and seleccion[0] > 0:  # Asegurarse de que no sea el primer elemento
                        del personaje.equipamiento[seleccion[0]]
                        cargar_equipamiento()

                ttk.Button(frame, text="Eliminar Equipamiento", command=eliminar_equipamiento).grid(row=2, column=0, columnspan=2, pady=5)

                ttk.Label(frame, text="Equipamiento disponible:").grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 5))
                equipamiento_disponible_listbox = tk.Listbox(frame, width=50, height=5)
                equipamiento_disponible_listbox.grid(row=4, column=0, columnspan=2, pady=(0, 10))

                def cargar_equipamiento_disponible():
                    equipamiento_disponible_listbox.delete(0, tk.END)
                    equipamiento_disponible = [e for e in Equipamiento.get_all() if e not in personaje.equipamiento]
                    for equipo in equipamiento_disponible:
                        equipamiento_disponible_listbox.insert(tk.END, equipo.Nombre_Equipamiento)

                cargar_equipamiento_disponible()

                def agregar_equipamiento():
                    seleccion = equipamiento_disponible_listbox.curselection()
                    if seleccion:
                        equipo_nombre = equipamiento_disponible_listbox.get(seleccion[0])
                        equipo = next((e for e in Equipamiento.get_all() if e.Nombre_Equipamiento == equipo_nombre), None)
                        if equipo and equipo not in personaje.equipamiento:
                            personaje.equipamiento.append(equipo)
                            cargar_equipamiento()
                            cargar_equipamiento_disponible()

                ttk.Button(frame, text="Agregar Equipamiento", command=agregar_equipamiento).grid(row=5, column=0, columnspan=2, pady=5)

                def guardar_cambios():
                    personaje.save()
                    self.cargar_personajes()
                    ventana_equipamiento.destroy()

                ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios).grid(row=6, column=0, columnspan=2, pady=10)

class CreadorPersonaje(tk.Toplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.usuario = usuario
        self.title("Crear Personaje")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        ttk.Label(left_frame, text="Nombre del Personaje:").pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ttk.Entry(left_frame, width=30)
        self.nombre_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(left_frame, text="Raza:").pack(anchor="w", pady=(0, 5))
        self.raza_combobox = ttk.Combobox(left_frame, state="readonly", width=28)
        self.raza_combobox.pack(fill=tk.X, pady=(0, 10))
        self.raza_combobox.bind("<<ComboboxSelected>>", self.actualizar_habilidades_poderes)

        ttk.Label(left_frame, text="Habilidades:").pack(anchor="w", pady=(0, 5))
        habilidades_frame = ttk.Frame(left_frame)
        habilidades_frame.pack(fill=tk.BOTH, expand=True)
        self.habilidades_listbox = tk.Listbox(habilidades_frame, selectmode=tk.MULTIPLE, width=40, height=10, exportselection=0)
        self.habilidades_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        habilidades_scrollbar = ttk.Scrollbar(habilidades_frame, orient="vertical", command=self.habilidades_listbox.yview)
        habilidades_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.habilidades_listbox.config(yscrollcommand=habilidades_scrollbar.set)

        ttk.Label(right_frame, text="Poder:").pack(anchor="w", pady=(0, 5))
        self.poder_combobox = ttk.Combobox(right_frame, state="readonly", width=28)
        self.poder_combobox.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_frame, text="Equipamiento:").pack(anchor="w", pady=(0, 5))
        equipamiento_frame = ttk.Frame(right_frame)
        equipamiento_frame.pack(fill=tk.BOTH, expand=True)
        self.equipamiento_listbox = tk.Listbox(equipamiento_frame, selectmode=tk.MULTIPLE, width=40, height=10, exportselection=0)
        self.equipamiento_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        equipamiento_scrollbar = ttk.Scrollbar(equipamiento_frame, orient="vertical", command=self.equipamiento_listbox.yview)
        equipamiento_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.equipamiento_listbox.config(yscrollcommand=equipamiento_scrollbar.set)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        ttk.Button(buttons_frame, text="Ver detalles de raza", command=self.ver_detalles_raza).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Ver detalles de habilidades", command=self.ver_detalles_habilidades).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Ver detalles de poder", command=self.ver_detalles_poder).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Ver detalles de equipamiento", command=self.ver_detalles_equipamiento).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Crear Personaje", command=self.crear_personaje).pack(side=tk.RIGHT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        razas = Raza.get_all()
        self.raza_combobox['values'] = [raza.Nombre_Raza for raza in razas]
        if razas:
            self.raza_combobox.set(razas[0].Nombre_Raza)
            self.actualizar_habilidades_poderes()

        equipamientos = Equipamiento.get_all()
        for equipo in equipamientos:
            self.equipamiento_listbox.insert(tk.END, equipo.Nombre_Equipamiento)

    def actualizar_habilidades_poderes(self, event=None):
        raza_nombre = self.raza_combobox.get()
        raza = Raza.get_by_nombre(raza_nombre)
        if raza:
            habilidades_seleccionadas = set(self.habilidades_listbox.curselection())
            self.habilidades_listbox.delete(0, tk.END)
            habilidades = Habilidad.get_by_raza(raza.ID_Raza)
            for i, habilidad in enumerate(habilidades):
                self.habilidades_listbox.insert(tk.END, habilidad.Nombre_Habilidad)
                if i in habilidades_seleccionadas:
                    self.habilidades_listbox.selection_set(i)

            self.poder_combobox['values'] = [poder.Nombre_Poder for poder in Poder.get_by_raza(raza.ID_Raza)]
            if self.poder_combobox['values']:
                self.poder_combobox.set(self.poder_combobox['values'][0])

    def ver_detalles_raza(self):
        raza_nombre = self.raza_combobox.get()
        raza = Raza.get_by_nombre(raza_nombre)
        if raza:
            messagebox.showinfo("Detalles de Raza", f"Nombre: {raza.Nombre_Raza}\nDescripción: {raza.Descripcion_Raza}")

    def ver_detalles_habilidades(self):
        detalles = ""
        for index in self.habilidades_listbox.curselection():
            habilidad = Habilidad.get_by_nombre(self.habilidades_listbox.get(index))
            if habilidad:
                detalles += f"Nombre: {habilidad.Nombre_Habilidad}\nDescripción: {habilidad.Descripcion_Habilidad}\n\n"
        if detalles:
            messagebox.showinfo("Detalles de Habilidades", detalles)
        else:
            messagebox.showinfo("Detalles de Habilidades", "No hay habilidades seleccionadas")

    def ver_detalles_poder(self):
        poder_nombre = self.poder_combobox.get()
        poder = Poder.get_by_nombre(poder_nombre)
        if poder:
            messagebox.showinfo("Detalles de Poder", f"Nombre: {poder.Nombre_Poder}\nDescripción: {poder.Descripcion_Poder}")

    def ver_detalles_equipamiento(self):
        seleccion = self.equipamiento_listbox.curselection()
        if seleccion:
            equipamientos = Equipamiento.get_all()
            detalles = ""
            for index in seleccion:
                equipo = equipamientos[index]
                detalles += f"Nombre: {equipo.Nombre_Equipamiento}\nDescripción: {equipo.Descripcion_Equipamiento}\n\n"
            messagebox.showinfo("Detalles de Equipamiento", detalles)

    def crear_personaje(self):
        nombre = self.nombre_entry.get()
        raza = Raza.get_by_nombre(self.raza_combobox.get())
        habilidades_seleccionadas = [Habilidad.get_by_nombre(self.habilidades_listbox.get(i)) for i in self.habilidades_listbox.curselection()]
        poder = Poder.get_by_nombre(self.poder_combobox.get())
        equipamiento_seleccionado = [Equipamiento.get_by_nombre(self.equipamiento_listbox.get(i)) for i in self.equipamiento_listbox.curselection()]

        if not nombre or not raza or len(habilidades_seleccionadas) != 2 or not poder or len(equipamiento_seleccionado) != 1:
            messagebox.showerror("Error", "Debes seleccionar un nombre, una raza, exactamente 2 habilidades, 1 poder y 1 equipamiento")
            return

        nuevo_personaje = Personaje(
             ID_Usuario=self.usuario.ID_Usuario,
             Nombre_Personaje=nombre,
             ID_Raza=raza.ID_Raza,
             Nivel=1,
             ID_Estado=1  # Vivo
        )
        nuevo_personaje.save()

        for habilidad in habilidades_seleccionadas:
            nuevo_personaje.agregar_habilidad(habilidad)

        nuevo_personaje.agregar_poder(poder)

        for equipo in equipamiento_seleccionado:
            nuevo_personaje.agregar_equipamiento(equipamiento_seleccionado[0])

        nuevo_personaje.save()

        messagebox.showinfo("Éxito", f"Personaje {nombre} creado con éxito")
        self.master.cargar_personajes()
        self.destroy()

class DetallesPersonaje(tk.Toplevel):
    def __init__(self, master, personaje):
        super().__init__(master)
        self.personaje = personaje
        self.title(f"Detalles de {personaje.Nombre_Personaje}")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Nombre del personaje
        ttk.Label(main_frame, text=f"Nombre: {self.personaje.Nombre_Personaje}", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        # Nivel
        ttk.Label(main_frame, text=f"Nivel: {self.personaje.Nivel}").pack(anchor="w", pady=(0, 5))

        # Raza
        raza = Raza.get_by_id(self.personaje.ID_Raza)
        ttk.Label(main_frame, text=f"Raza: {raza.Nombre_Raza}").pack(anchor="w", pady=(0, 5))

        # Estado
        estado = Estado.get_by_id(self.personaje.ID_Estado)
        ttk.Label(main_frame, text=f"Estado: {estado.Nombre_Estado}").pack(anchor="w", pady=(0, 5))

        # Habilidades
        ttk.Label(main_frame, text="Habilidades:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        for habilidad in self.personaje.habilidades:
            ttk.Label(main_frame, text=f"- {habilidad.Nombre_Habilidad}: {habilidad.Descripcion_Habilidad}").pack(anchor="w", padx=(20, 0))

        # Poder
        ttk.Label(main_frame, text="Poder:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        if self.personaje.poder:
            ttk.Label(main_frame, text=f"- {self.personaje.poder.Nombre_Poder}: {self.personaje.poder.Descripcion_Poder}").pack(anchor="w", padx=(20, 0))
        else:
            ttk.Label(main_frame, text="- Ningún poder asignado").pack(anchor="w", padx=(20, 0))

        # Equipamiento
        ttk.Label(main_frame, text="Equipamiento:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        equipamiento = Equipamiento.get_by_personaje(self.personaje.ID_Personaje)
        if equipamiento:
            for equipo in equipamiento:
                ttk.Label(main_frame, text=f"- {equipo.Nombre_Equipamiento}: {equipo.Descripcion_Equipamiento}").pack(anchor="w", padx=(20, 0))
        else:
            ttk.Label(main_frame, text="- Ningún equipamiento asignado").pack(anchor="w", padx=(20, 0))

        # Botón para cerrar
        ttk.Button(main_frame, text="Cerrar", command=self.destroy).pack(pady=(20, 0))    

class GestionHabilidades(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Habilidades")
        self.create_widgets()

    def create_widgets(self):
        self.habilidades_listbox = tk.Listbox(self, width=50)
        self.habilidades_listbox.pack(pady=10)

        self.raza_label = ttk.Label(self, text="Raza:")
        self.raza_label.pack()
        self.raza_combobox = ttk.Combobox(self, state="readonly")
        self.raza_combobox.pack(pady=5)
        self.raza_combobox.bind("<<ComboboxSelected>>", self.cargar_habilidades_por_raza)

        self.cargar_razas()

        ttk.Button(self, text="Agregar Habilidad", command=self.agregar_habilidad).pack(pady=5)
        ttk.Button(self, text="Modificar Habilidad", command=self.modificar_habilidad).pack(pady=5)
        ttk.Button(self, text="Eliminar Habilidad", command=self.eliminar_habilidad).pack(pady=5)

    def cargar_razas(self):
        razas = Raza.get_all()
        self.raza_combobox['values'] = [raza.Nombre_Raza for raza in razas]
        if razas:
            self.raza_combobox.set(razas[0].Nombre_Raza)
            self.cargar_habilidades_por_raza()

    def cargar_habilidades_por_raza(self, event=None):
        raza_nombre = self.raza_combobox.get()
        raza = Raza.get_by_nombre(raza_nombre)
        if raza:
            self.habilidades_listbox.delete(0, tk.END)
            habilidades = Habilidad.get_by_raza(raza.ID_Raza)
            for habilidad in habilidades:
                self.habilidades_listbox.insert(tk.END, f"{habilidad.Nombre_Habilidad} - {habilidad.Descripcion_Habilidad}")

    def agregar_habilidad(self):
        if not self.raza_combobox.get():
            messagebox.showerror("Error", "Debes seleccionar una raza")
            return

        nombre = simpledialog.askstring("Agregar Habilidad", "Nombre de la habilidad:")
        if nombre:
            descripcion = simpledialog.askstring("Agregar Habilidad", "Descripción de la habilidad:")
            if descripcion:
                raza_nombre = self.raza_combobox.get()
                id_raza = Raza.get_by_nombre(raza_nombre).ID_Raza
                nueva_habilidad = Habilidad(Nombre_Habilidad=nombre, Descripcion_Habilidad=descripcion, ID_Raza=id_raza)
                nueva_habilidad.save()
                self.cargar_habilidades_por_raza()

    def modificar_habilidad(self):
        seleccion = self.habilidades_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            raza_nombre = self.raza_combobox.get()
            raza = Raza.get_by_nombre(raza_nombre)
            habilidad_actual = Habilidad.get_by_raza(raza.ID_Raza)[index]
            nuevo_nombre = simpledialog.askstring("Modificar Habilidad", "Nuevo nombre:", initialvalue=habilidad_actual.Nombre_Habilidad)
            if nuevo_nombre:
                nueva_descripcion = simpledialog.askstring("Modificar Habilidad", "Nueva descripción:", initialvalue=habilidad_actual.Descripcion_Habilidad)
                if nueva_descripcion:
                    habilidad_actual.Nombre_Habilidad = nuevo_nombre
                    habilidad_actual.Descripcion_Habilidad = nueva_descripcion
                    habilidad_actual.save()
                    self.cargar_habilidades_por_raza()

    def eliminar_habilidad(self):
        seleccion = self.habilidades_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            raza_nombre = self.raza_combobox.get()
            raza = Raza.get_by_nombre(raza_nombre)
            habilidad_a_eliminar = Habilidad.get_by_raza(raza.ID_Raza)[index]
            confirmacion = messagebox.askyesno("Eliminar Habilidad", f"¿Estás seguro de que quieres eliminar la habilidad '{habilidad_a_eliminar.Nombre_Habilidad}'?")
            if confirmacion:
                habilidad_a_eliminar.delete()
                self.cargar_habilidades_por_raza()


class GestionPoderes(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Poderes")
        self.create_widgets()

    def create_widgets(self):
        self.poderes_listbox = tk.Listbox(self, width=50)
        self.poderes_listbox.pack(pady=10)

        self.raza_label = ttk.Label(self, text="Raza:")
        self.raza_label.pack()
        self.raza_combobox = ttk.Combobox(self, state="readonly")
        self.raza_combobox.pack(pady=5)
        self.raza_combobox.bind("<<ComboboxSelected>>", self.cargar_poderes_por_raza)

        self.cargar_razas()

        ttk.Button(self, text="Agregar Poder", command=self.agregar_poder).pack(pady=5)
        ttk.Button(self, text="Modificar Poder", command=self.modificar_poder).pack(pady=5)
        ttk.Button(self, text="Eliminar Poder", command=self.eliminar_poder).pack(pady=5)

    def cargar_razas(self):
        razas = Raza.get_all()
        self.raza_combobox['values'] = [raza.Nombre_Raza for raza in razas]
        if razas:
            self.raza_combobox.set(razas[0].Nombre_Raza)
            self.cargar_poderes_por_raza()

    def cargar_poderes_por_raza(self, event=None):
        raza_nombre = self.raza_combobox.get()
        raza = Raza.get_by_nombre(raza_nombre)
        if raza:
            self.poderes_listbox.delete(0, tk.END)
            poderes = Poder.get_by_raza(raza.ID_Raza)
            for poder in poderes:
                self.poderes_listbox.insert(tk.END, f"{poder.Nombre_Poder} - {poder.Descripcion_Poder}")

    def agregar_poder(self):
        if not self.raza_combobox.get():
            messagebox.showerror("Error", "Debes seleccionar una raza")
            return

        nombre = simpledialog.askstring("Agregar Poder", "Nombre del poder:")
        if nombre:
            descripcion = simpledialog.askstring("Agregar Poder", "Descripción del poder:")
            if descripcion:
                raza_nombre = self.raza_combobox.get()
                id_raza = Raza.get_by_nombre(raza_nombre).ID_Raza
                nuevo_poder = Poder(Nombre_Poder=nombre, Descripcion_Poder=descripcion, ID_Raza=id_raza)
                nuevo_poder.save()
                self.cargar_poderes_por_raza()

    def modificar_poder(self):
        seleccion = self.poderes_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            raza_nombre = self.raza_combobox.get()
            raza = Raza.get_by_nombre(raza_nombre)
            poder_actual = Poder.get_by_raza(raza.ID_Raza)[index]
            nuevo_nombre = simpledialog.askstring("Modificar Poder", "Nuevo nombre:", initialvalue=poder_actual.Nombre_Poder)
            if nuevo_nombre:
                nueva_descripcion = simpledialog.askstring("Modificar Poder", "Nueva descripción:", initialvalue=poder_actual.Descripcion_Poder)
                if nueva_descripcion:
                    poder_actual.Nombre_Poder = nuevo_nombre
                    poder_actual.Descripcion_Poder = nueva_descripcion
                    poder_actual.save()
                    self.cargar_poderes_por_raza()

    def eliminar_poder(self):
        seleccion = self.poderes_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            raza_nombre = self.raza_combobox.get()
            raza = Raza.get_by_nombre(raza_nombre)
            poder_a_eliminar = Poder.get_by_raza(raza.ID_Raza)[index]
            confirmacion = messagebox.askyesno("Eliminar Poder", f"¿Estás seguro de que quieres eliminar el poder '{poder_a_eliminar.Nombre_Poder}'?")
            if confirmacion:
                poder_a_eliminar.delete()
                self.cargar_poderes_por_raza()


class GestionRazasGM(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Razas por GM")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Selecciona una raza:").pack(pady=10)
        self.raza_combobox = ttk.Combobox(self, state="readonly")
        self.raza_combobox.pack(pady=5)

        ttk.Button(self, text="Agregar Raza", command=self.agregar_raza).pack(pady=5)
        ttk.Button(self, text="Modificar Raza", command=self.modificar_raza).pack(pady=5)
        ttk.Button(self, text="Eliminar Raza", command=self.eliminar_raza).pack(pady=5)

        self.cargar_razas()

    def cargar_razas(self):
        # Lógica para cargar las razas disponibles
        razas = Raza.get_all()
        self.raza_combobox['values'] = [raza.Nombre_Raza for raza in razas]

    def agregar_raza(self):
        # Lógica para agregar una nueva raza
        nombre_raza = simpledialog.askstring("Crear Raza", "Ingrese el nombre de la nueva raza:")
        if nombre_raza:
            descripcion_raza = simpledialog.askstring("Crear Raza", "Ingrese la descripción de la nueva raza:")
            if descripcion_raza:
                nueva_raza = Raza(Nombre_Raza=nombre_raza, Descripcion_Raza=descripcion_raza)
                nueva_raza.save()
                self.cargar_razas()

    def modificar_raza(self):
        # Lógica para modificar una raza existente
        nombre_raza_seleccionada = self.raza_combobox.get()
        if nombre_raza_seleccionada:
            raza_seleccionada = next((raza for raza in Raza.get_all() if raza.Nombre_Raza == nombre_raza_seleccionada), None)
            if raza_seleccionada:
                nuevo_nombre = simpledialog.askstring("Modificar Raza", f"Ingrese el nuevo nombre para '{raza_seleccionada.Nombre_Raza}':")
                if nuevo_nombre:
                    nueva_descripcion = simpledialog.askstring("Modificar Raza", f"Ingrese la nueva descripción para '{raza_seleccionada.Nombre_Raza}':")
                    raza_seleccionada.Nombre_Raza = nuevo_nombre
                    raza_seleccionada.Descripcion_Raza = nueva_descripcion
                    raza_seleccionada.save()
                    self.cargar_razas()

    def eliminar_raza(self):
        # Lógica para eliminar una raza existente
        nombre_raza_seleccionada = self.raza_combobox.get()
        if nombre_raza_seleccionada:
            raza_seleccionada = next((raza for raza in Raza.get_all() if raza.Nombre_Raza == nombre_raza_seleccionada), None)
            if raza_seleccionada:
                confirmacion = messagebox.askyesno("Eliminar Raza", f"¿Está seguro que desea eliminar la raza '{raza_seleccionada.Nombre_Raza}'?")
                if confirmacion:
                    raza_seleccionada.delete()
                    self.cargar_razas()

class GestionEquipamiento(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Equipamiento")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Equipamiento:").pack(pady=5)
        self.equipamiento_listbox = tk.Listbox(self, width=50)
        self.equipamiento_listbox.pack(pady=5)
        self.cargar_equipamiento()

        ttk.Button(self, text="Agregar Equipamiento", command=self.agregar_equipamiento).pack(pady=5)
        ttk.Button(self, text="Modificar Nombre", command=self.modificar_nombre_equipamiento).pack(pady=5)

    def cargar_equipamiento(self):
        self.equipamiento_listbox.delete(0, tk.END)
        equipamientos = Equipamiento.get_all()
        for equip in equipamientos:
            self.equipamiento_listbox.insert(tk.END, f"{equip.Nombre_Equipamiento} - {equip.Descripcion_Equipamiento}")

    def agregar_equipamiento(self):
        nombre = simpledialog.askstring("Agregar Equipamiento", "Nombre del equipamiento:")
        if nombre:
            descripcion = simpledialog.askstring("Agregar Equipamiento", "Descripción del equipamiento:")
            if descripcion:
                nuevo_equipamiento = Equipamiento(Nombre_Equipamiento=nombre, Descripcion_Equipamiento=descripcion)
                nuevo_equipamiento.save()
                self.cargar_equipamiento()

    def modificar_nombre_equipamiento(self):
        seleccion = self.equipamiento_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            equipamiento = Equipamiento.get_all()[index]
            nuevo_nombre = simpledialog.askstring("Modificar Nombre", f"Nombre actual: {equipamiento.Nombre_Equipamiento}\nNuevo nombre:")
            if nuevo_nombre:
                equipamiento.Nombre_Equipamiento = nuevo_nombre
                equipamiento.save()
                self.cargar_equipamiento()
                
    def cargar_personajes(self):
        personajes = Personaje.get_all()
        for personaje in personajes:
            raza = Raza.get_by_id(personaje.ID_Raza)
            self.personajes_listbox.insert(tk.END, f"{personaje.Nombre_Personaje} - Nivel: {personaje.Nivel} - Raza: {raza.Nombre_Raza}")

    def ver_detalles_personaje(self):
        seleccion = self.personajes_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            personaje = Personaje.get_all()[index]
            raza = Raza.get_by_id(personaje.ID_Raza)
            habilidades = Habilidad.get_by_raza(raza.ID_Raza)
            poderes = Poder.get_by_raza(raza.ID_Raza)
            
            detalles = f"Nombre: {personaje.Nombre_Personaje}\n"
            detalles += f"Nivel: {personaje.Nivel}\n"
            detalles += f"Raza: {raza.Nombre_Raza}\n\n"
            detalles += "Habilidades de la raza:\n"
            for habilidad in habilidades:
                detalles += f"- {habilidad.Nombre_Habilidad}: {habilidad.Descripcion_Habilidad}\n"
            detalles += "\nPoderes de la raza:\n"
            for poder in poderes:
                detalles += f"- {poder.Nombre_Poder}: {poder.Descripcion_Poder}\n"

            messagebox.showinfo("Detalles del Personaje", detalles)


class GMModificadorPersonaje(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Modificar Personaje (GM)")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de personajes
        ttk.Label(main_frame, text="Selecciona un personaje:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.personajes_listbox = tk.Listbox(main_frame, width=50, height=10)
        self.personajes_listbox.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.cargar_personajes()

        # Botones de acción
        ttk.Button(main_frame, text="Modificar Nivel", command=self.modificar_nivel).grid(row=2, column=0, pady=5)
        ttk.Button(main_frame, text="Modificar Raza", command=self.modificar_raza).grid(row=2, column=1, pady=5)
        ttk.Button(main_frame, text="Modificar Habilidades", command=self.modificar_habilidades).grid(row=3, column=0, pady=5)
        ttk.Button(main_frame, text="Modificar Poder", command=self.modificar_poder).grid(row=3, column=1, pady=5)
        ttk.Button(main_frame, text="Modificar Equipamiento", command=self.modificar_equipamiento).grid(row=4, column=0, pady=5)
        ttk.Button(main_frame, text="Modificar Estado", command=self.modificar_estado).grid(row=4, column=1, pady=5)
        ttk.Button(main_frame, text="Ver Detalles", command=self.ver_detalles_personaje).grid(row=1, column=2, pady=5, padx=10, sticky="ns")

    def cargar_personajes(self):
        self.personajes_listbox.delete(0, tk.END)
        personajes = Personaje.get_all()
        for personaje in personajes:
            estado = Estado.get_by_id(personaje.ID_Estado)
            self.personajes_listbox.insert(tk.END, f"{personaje.Nombre_Personaje} (Nivel {personaje.Nivel}, Estado: {estado.Nombre_Estado if estado else 'Desconocido'})")

    def obtener_personaje_seleccionado(self):
        seleccion = self.personajes_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            return Personaje.get_all()[index]
        return None

    def modificar_nivel(self):
        personaje = self.obtener_personaje_seleccionado()
        if personaje:
            nuevo_nivel = simpledialog.askinteger("Modificar Nivel", f"Nivel actual de {personaje.Nombre_Personaje}: {personaje.Nivel}\nNuevo nivel:", minvalue=1, maxvalue=20)
            if nuevo_nivel:
                personaje.Nivel = nuevo_nivel
                personaje.save()
                self.cargar_personajes()

    def modificar_raza(self):
        personaje = self.obtener_personaje_seleccionado()
        if not personaje:
            return

        razas = Raza.get_all()
        raza_actual = Raza.get_by_id(personaje.ID_Raza)

        ventana_razas = tk.Toplevel(self)
        ventana_razas.title(f"Modificar Raza de {personaje.Nombre_Personaje}")

        ttk.Label(ventana_razas, text="Selecciona la nueva raza:").pack(pady=5)
        razas_listbox = tk.Listbox(ventana_razas, width=50, height=10)
        razas_listbox.pack(pady=5)

        for raza in razas:
            razas_listbox.insert(tk.END, raza.Nombre_Raza)
            if raza.ID_Raza == personaje.ID_Raza:
                razas_listbox.selection_set(razas.index(raza))
                
                
        def guardar_cambios():
            seleccion = razas_listbox.curselection()
            if seleccion:
                nueva_raza = razas[seleccion[0]]
                personaje.ID_Raza = nueva_raza.ID_Raza
                personaje.save()
                self.cargar_personajes()
                ventana_razas.destroy()

        ttk.Button(ventana_razas, text="Guardar", command=guardar_cambios).pack(pady=10)

    def modificar_habilidades(self):
        personaje = self.obtener_personaje_seleccionado()
        if not personaje:
            messagebox.showerror("Error", "Por favor, seleccione un personaje.")
            return

        ventana_habilidades = tk.Toplevel(self)
        ventana_habilidades.title(f"Modificar Habilidades de {personaje.Nombre_Personaje}")
        ventana_habilidades.geometry("600x400")

        frame = ttk.Frame(ventana_habilidades, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Habilidades del personaje:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        habilidades_personaje_listbox = tk.Listbox(frame, width=50, height=5)
        habilidades_personaje_listbox.grid(row=1, column=0, pady=(0, 10))

        ttk.Label(frame, text="Habilidades disponibles:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        habilidades_disponibles_listbox = tk.Listbox(frame, width=50, height=5)
        habilidades_disponibles_listbox.grid(row=3, column=0, pady=(0, 10))

        def actualizar_listas():
            habilidades_personaje_listbox.delete(0, tk.END)
            habilidades_disponibles_listbox.delete(0, tk.END)
        
            for i, habilidad in enumerate(personaje.habilidades):
                habilidades_personaje_listbox.insert(tk.END, habilidad.Nombre_Habilidad)
                if i < 2:
                    habilidades_personaje_listbox.itemconfig(i, {'bg': 'light gray'})

            habilidades_raza = Habilidad.get_by_raza(personaje.ID_Raza)
            for habilidad in habilidades_raza:
                if habilidad not in personaje.habilidades:
                    habilidades_disponibles_listbox.insert(tk.END, habilidad.Nombre_Habilidad)

        actualizar_listas()

        def agregar_habilidad():
            if len(personaje.habilidades) >= 8:
                messagebox.showwarning("Advertencia", "El personaje ya tiene el máximo de 8 habilidades.")
                return

            seleccion = habilidades_disponibles_listbox.curselection()
            if seleccion:
                index = seleccion[0]
                habilidad_nombre = habilidades_disponibles_listbox.get(index)
                habilidad = next((h for h in Habilidad.get_by_raza(personaje.ID_Raza) if h.Nombre_Habilidad == habilidad_nombre), None)
                if habilidad:
                    personaje.agregar_habilidad(habilidad)
                    actualizar_listas()

        def quitar_habilidad():
            seleccion = habilidades_personaje_listbox.curselection()
            if seleccion and seleccion[0] >= 2:
                index = seleccion[0]
                habilidad = personaje.habilidades[index]
                personaje.eliminar_habilidad(habilidad)
                actualizar_listas()

        ttk.Button(frame, text="Agregar Habilidad", command=agregar_habilidad).grid(row=4, column=0, pady=5)
        ttk.Button(frame, text="Quitar Habilidad", command=quitar_habilidad).grid(row=5, column=0, pady=5)

        def guardar_cambios():
            personaje.save()
            messagebox.showinfo("Éxito", "Habilidades actualizadas correctamente.")
            ventana_habilidades.destroy()

        ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios).grid(row=6, column=0, pady=10)
        
    def modificar_estado(self):
        personaje = self.obtener_personaje_seleccionado()
        if personaje:
            estados = Estado.get_all()
            estado_actual = Estado.get_by_id(personaje.ID_Estado)
            ventana_estados = tk.Toplevel(self)
            ventana_estados.title(f"Modificar Estado de {personaje.Nombre_Personaje}")
            ttk.Label(ventana_estados, text="Selecciona el nuevo estado:").pack(pady=5)
            estados_listbox = tk.Listbox(ventana_estados, width=50, height=10)
            estados_listbox.pack(pady=5)

            for estado in estados:
                estados_listbox.insert(tk.END, estado.Nombre_Estado)
                if estado.ID_Estado == personaje.ID_Estado:
                    estados_listbox.selection_set(estados.index(estado))
        
            def guardar_cambios():
                seleccion = estados_listbox.curselection()
                if seleccion:
                    nuevo_estado = estados[seleccion[0]]
                    personaje.ID_Estado = nuevo_estado.ID_Estado
                    personaje.save()
                    self.cargar_personajes()
                    ventana_estados.destroy()
            ttk.Button(ventana_estados, text="Guardar", command=guardar_cambios).pack(pady=10)

    def modificar_poder(self):
        personaje = self.obtener_personaje_seleccionado()
        if not personaje:
            return
            
        poderes = Poder.get_by_raza(personaje.ID_Raza)
        poder_actual = personaje.poder

        ventana_poderes = tk.Toplevel(self)
        ventana_poderes.title(f"Modificar Poder de {personaje.Nombre_Personaje}")

        ttk.Label(ventana_poderes, text="Selecciona el nuevo poder:").pack(pady=5)
        poderes_listbox = tk.Listbox(ventana_poderes, width=50, height=10)
        poderes_listbox.pack(pady=5)

        for poder in poderes:
            poderes_listbox.insert(tk.END, poder.Nombre_Poder)
            if poder == poder_actual:
                poderes_listbox.selection_set(poderes.index(poder))

        def guardar_cambios():
            seleccion = poderes_listbox.curselection()
            if seleccion:
                nuevo_poder = poderes[seleccion[0]]
                personaje.agregar_poder(nuevo_poder)
                personaje.save()
                self.cargar_personajes()
                ventana_poderes.destroy()
        ttk.Button(ventana_poderes, text="Guardar", command=guardar_cambios).pack(pady=10)

    def modificar_equipamiento(self):
        personaje = self.obtener_personaje_seleccionado()
        if not personaje:
            messagebox.showerror("Error", "Por favor, seleccione un personaje.")
            return

        if personaje.ID_Estado == 2:  # Asumiendo que 2 es el ID del estado "Muerto"
            messagebox.showerror("Error", "No se puede modificar el equipamiento de un personaje muerto.")
            return

        ventana_equipamiento = tk.Toplevel(self)
        ventana_equipamiento.title(f"Modificar Equipamiento de {personaje.Nombre_Personaje}")
        ventana_equipamiento.geometry("600x400")

        frame = ttk.Frame(ventana_equipamiento, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Equipamiento actual:").grid(row=0, column=0, sticky="w", pady=5)
        equipamiento_listbox = tk.Listbox(frame, width=50, height=8)
        equipamiento_listbox.grid(row=1, column=0, pady=5)

        ttk.Label(frame, text="Equipamiento disponible:").grid(row=0, column=1, sticky="w", pady=5)
        equipamiento_disponible_listbox = tk.Listbox(frame, width=50, height=8)
        equipamiento_disponible_listbox.grid(row=1, column=1, pady=5)
 
        def cargar_equipamiento():
            equipamiento_listbox.delete(0, tk.END)
            for i, equipo in enumerate(personaje.equipamiento):
                equipamiento_listbox.insert(tk.END, equipo.Nombre_Equipamiento)
                if i == 0:  # El primer equipamiento no se puede eliminar
                    equipamiento_listbox.itemconfig(i, {'bg': 'light gray'})

        def cargar_equipamiento_disponible():
            equipamiento_disponible_listbox.delete(0, tk.END)
            equipamiento_disponible = [e for e in Equipamiento.get_all() if e not in personaje.equipamiento]
            for equipo in equipamiento_disponible:
                equipamiento_disponible_listbox.insert(tk.END, equipo.Nombre_Equipamiento)

        cargar_equipamiento()
        cargar_equipamiento_disponible()

        def agregar_equipamiento():
            if len(personaje.equipamiento) >= 8:
                messagebox.showwarning("Advertencia", "El personaje ya tiene el máximo de 8 equipamientos.")
                return

            seleccion = equipamiento_disponible_listbox.curselection()
            if seleccion:
                index = seleccion[0]
                equipo_nombre = equipamiento_disponible_listbox.get(index)
                equipo = next((e for e in Equipamiento.get_all() if e.Nombre_Equipamiento == equipo_nombre), None)
                if equipo:
                    personaje.equipamiento.append(equipo)
                    cargar_equipamiento()
                    cargar_equipamiento_disponible()

        def eliminar_equipamiento():
            seleccion = equipamiento_listbox.curselection()
            if seleccion and seleccion[0] > 0:  # No se puede eliminar el primer equipamiento
                del personaje.equipamiento[seleccion[0]]
                cargar_equipamiento()
                cargar_equipamiento_disponible()

        ttk.Button(frame, text="Agregar Equipamiento", command=agregar_equipamiento).grid(row=2, column=1, pady=5)
        ttk.Button(frame, text="Eliminar Equipamiento", command=eliminar_equipamiento).grid(row=2, column=0, pady=5)

        def guardar_cambios():
            personaje.save()
            self.cargar_personajes()
            messagebox.showinfo("Éxito", "Equipamiento actualizado correctamente.")
            ventana_equipamiento.destroy()

        ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios).grid(row=3, column=0, columnspan=2, pady=10)

    def ver_detalles_personaje(self):
        personaje = self.obtener_personaje_seleccionado()
        if not personaje:
            return

        ventana_detalles = tk.Toplevel(self)
        ventana_detalles.title(f"Detalles de {personaje.Nombre_Personaje}")

        frame = ttk.Frame(ventana_detalles, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=f"Nombre: {personaje.Nombre_Personaje}", font=("", 12, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(frame, text=f"Nivel: {personaje.Nivel}").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(frame, text=f"Raza: {Raza.get_by_id(personaje.ID_Raza).Nombre_Raza}").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(frame, text=f"Estado: {Estado.get_by_id(personaje.ID_Estado).Nombre_Estado}").grid(row=3, column=0, sticky="w", pady=2)

        ttk.Label(frame, text="Habilidades:", font=("", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10, 5))
        habilidades_text = "\n".join([f"- {h.Nombre_Habilidad}" for h in personaje.habilidades])
        ttk.Label(frame, text=habilidades_text).grid(row=5, column=0, sticky="w", pady=2)

        ttk.Label(frame, text="Poder:", font=("", 10, "bold")).grid(row=6, column=0, sticky="w", pady=(10, 5))
        poder_text = f"- {personaje.poder.Nombre_Poder}" if personaje.poder else "- Ningún poder asignado"
        ttk.Label(frame, text=poder_text).grid(row=7, column=0, sticky="w", pady=2)

        ttk.Label(frame, text="Equipamiento:", font=("", 10, "bold")).grid(row=8, column=0, sticky="w", pady=(10, 5))
        personaje.cargar_equipamiento()
        equipamiento_text = "\n".join([f"- {e.Nombre_Equipamiento}" for e in personaje.equipamiento])
        ttk.Label(frame, text=equipamiento_text).grid(row=9, column=0, sticky="w", pady=2)

        ttk.Button(frame, text="Cerrar", command=ventana_detalles.destroy).grid(row=10, column=0, pady=10)

        
class GestionEstados(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Estados")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.estados_listbox = tk.Listbox(self, width=50, height=10)
        self.estados_listbox.pack(pady=10)
        self.cargar_estados()

        ttk.Button(self, text="Agregar Estado", command=self.agregar_estado).pack(pady=5)
        ttk.Button(self, text="Modificar Estado", command=self.modificar_estado).pack(pady=5)
        ttk.Button(self, text="Eliminar Estado", command=self.eliminar_estado).pack(pady=5)

    def cargar_estados(self):
        self.estados_listbox.delete(0, tk.END)
        estados = Estado.get_all()
        for estado in estados:
            self.estados_listbox.insert(tk.END, f"{estado.Nombre_Estado} ({'Base' if estado.Es_Base else 'Personalizado'})")

    def agregar_estado(self):
        nombre = simpledialog.askstring("Agregar Estado", "Nombre del nuevo estado:")
        if nombre:
            descripcion = simpledialog.askstring("Agregar Estado", "Descripción del estado:")
            nuevo_estado = Estado(Nombre_Estado=nombre, Descripcion_Estado=descripcion)
            nuevo_estado.save()
            self.cargar_estados()

    def modificar_estado(self):
        seleccion = self.estados_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            estado = Estado.get_all()[index]
            if not estado.Es_Base:
                nuevo_nombre = simpledialog.askstring("Modificar Estado", "Nuevo nombre del estado:", initialvalue=estado.Nombre_Estado)
                if nuevo_nombre:
                    nueva_descripcion = simpledialog.askstring("Modificar Estado", "Nueva descripción del estado:", initialvalue=estado.Descripcion_Estado)
                    estado.Nombre_Estado = nuevo_nombre
                    estado.Descripcion_Estado = nueva_descripcion
                    estado.save()
                    self.cargar_estados()
            else:
                messagebox.showwarning("Modificar Estado", "No se pueden modificar los estados base.")

    def eliminar_estado(self):
        seleccion = self.estados_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            estado = Estado.get_all()[index]
            if not estado.Es_Base:
                confirmacion = messagebox.askyesno("Eliminar Estado", f"¿Estás seguro de que quieres eliminar el estado '{estado.Nombre_Estado}'?")
                if confirmacion:
                    try:
                        estado.delete()
                        self.cargar_estados()
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Eliminar Estado", "No se pueden eliminar los estados base.")