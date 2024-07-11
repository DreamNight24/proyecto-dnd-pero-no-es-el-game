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
        ttk.Button(self, text="Ver Informe de Personajes", command=self.ver_informe).pack(pady=5)

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

    def ver_informe(self):
        InformePersonajes(self)


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
        ttk.Button(self.modificar_equipamiento_frame, text="Modificar Equipamiento", command=self.abrir_modificador_equipamiento).pack(pady=10)

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

    def abrir_modificador_equipamiento(self):
        personaje_nombre = self.personajes_equipamiento_combobox.get()
        if personaje_nombre:
            personaje = next((p for p in Personaje.get_by_usuario(self.usuario.ID_Usuario) if p.Nombre_Personaje == personaje_nombre), None)
            if personaje:
                ModificadorEquipamiento(self, personaje)

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

        # Nombre del Personaje
        ttk.Label(left_frame, text="Nombre del Personaje:").pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ttk.Entry(left_frame, width=30)
        self.nombre_entry.pack(fill=tk.X, pady=(0, 10))

        # Raza
        ttk.Label(left_frame, text="Raza:").pack(anchor="w", pady=(0, 5))
        self.raza_combobox = ttk.Combobox(left_frame, state="readonly", width=28)
        self.raza_combobox.pack(fill=tk.X, pady=(0, 10))
        self.raza_combobox.bind("<<ComboboxSelected>>", self.actualizar_habilidades_poderes)

        # Habilidades
        ttk.Label(left_frame, text="Habilidades:").pack(anchor="w", pady=(0, 5))
        habilidades_frame = ttk.Frame(left_frame)
        habilidades_frame.pack(fill=tk.BOTH, expand=True)
        self.habilidades_listbox = tk.Listbox(habilidades_frame, selectmode=tk.MULTIPLE, width=40, height=10, exportselection=0)
        self.habilidades_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        habilidades_scrollbar = ttk.Scrollbar(habilidades_frame, orient="vertical", command=self.habilidades_listbox.yview)
        habilidades_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.habilidades_listbox.config(yscrollcommand=habilidades_scrollbar.set)

        # Poder
        ttk.Label(right_frame, text="Poder:").pack(anchor="w", pady=(0, 5))
        self.poder_combobox = ttk.Combobox(right_frame, state="readonly", width=28)
        self.poder_combobox.pack(fill=tk.X, pady=(0, 10))

        # Equipamiento
        ttk.Label(right_frame, text="Equipamiento:").pack(anchor="w", pady=(0, 5))
        equipamiento_frame = ttk.Frame(right_frame)
        equipamiento_frame.pack(fill=tk.BOTH, expand=True)
        self.equipamiento_listbox = tk.Listbox(equipamiento_frame, selectmode=tk.MULTIPLE, width=40, height=10, exportselection=0)
        self.equipamiento_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        equipamiento_scrollbar = ttk.Scrollbar(equipamiento_frame, orient="vertical", command=self.equipamiento_listbox.yview)
        equipamiento_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.equipamiento_listbox.config(yscrollcommand=equipamiento_scrollbar.set)

        # Botones de detalles
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

        if not nombre or not raza or not habilidades_seleccionadas or not poder or not equipamiento_seleccionado:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
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
            nuevo_personaje.agregar_habilidad(habilidad.ID_Habilidad)

        nuevo_personaje.agregar_poder(poder.ID_Poder)

        for equipo in equipamiento_seleccionado:
            Personaje_Equipamiento(ID_Personaje=nuevo_personaje.ID_Personaje, ID_Equipamiento=equipo.ID_Equipamiento).save()

        messagebox.showinfo("Éxito", f"Personaje {nombre} creado con éxito")
        self.master.cargar_personajes()  # Actualizar la lista de personajes en la interfaz del jugador
        self.destroy()

        for habilidad in habilidades_seleccionadas:
            nuevo_personaje.agregar_habilidad(habilidad.ID_Habilidad)

        nuevo_personaje.agregar_poder(poder.ID_Poder)

        for equipo in equipamiento_seleccionado:
            Personaje_Equipamiento(ID_Personaje=nuevo_personaje.ID_Personaje, ID_Equipamiento=equipo.ID_Equipamiento).save()

        messagebox.showinfo("Éxito", f"Personaje {nombre} creado con éxito")
        self.master.cargar_personajes()  # Actualizar la lista de personajes en la interfaz del jugador
        self.destroy()

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
        ttk.Button(self, text="Eliminar Equipamiento", command=self.eliminar_equipamiento).pack(pady=5)

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

    def eliminar_equipamiento(self):
        seleccion = self.equipamiento_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            equipamiento = Equipamiento.get_all()[index]
            confirmacion = messagebox.askyesno("Eliminar Equipamiento", f"¿Estás seguro de que quieres eliminar el equipamiento '{equipamiento.Nombre_Equipamiento}'?")
            if confirmacion:
                equipamiento.delete()
                self.cargar_equipamiento()
                

class InformePersonajes(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Informe de Personajes")
        self.create_widgets()

    def create_widgets(self):
        self.personajes_listbox = tk.Listbox(self, width=100, height=20)
        self.personajes_listbox.pack(pady=10)
        self.cargar_personajes()

        ttk.Button(self, text="Ver Detalles", command=self.ver_detalles_personaje).pack(pady=5)

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
        ttk.Button(main_frame, text="Modificar Equipamiento", command=self.modificar_equipamiento).grid(row=4, column=0, columnspan=2, pady=5)

    def cargar_personajes(self):
        self.personajes_listbox.delete(0, tk.END)
        personajes = Personaje.get_all()
        for personaje in personajes:
            self.personajes_listbox.insert(tk.END, f"{personaje.Nombre_Personaje} (Nivel {personaje.Nivel})")

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
        if personaje:
            razas = Raza.get_all()
            raza_actual = Raza.get_by_id(personaje.ID_Raza)
            opciones = [raza.Nombre_Raza for raza in razas]
            nueva_raza = simpledialog.askstring("Modificar Raza", f"Raza actual de {personaje.Nombre_Personaje}: {raza_actual.Nombre_Raza}\nSelecciona la nueva raza:", initialvalue=raza_actual.Nombre_Raza)
            if nueva_raza in opciones:
                personaje.ID_Raza = next(raza.ID_Raza for raza in razas if raza.Nombre_Raza == nueva_raza)
                personaje.save()

    def modificar_habilidades(self):
        personaje = self.obtener_personaje_seleccionado()
        if personaje:
            ModificadorHabilidades(self, personaje)

    def modificar_poder(self):
        personaje = self.obtener_personaje_seleccionado()
        if personaje:
            poderes = Poder.get_by_raza(personaje.ID_Raza)
            opciones = [poder.Nombre_Poder for poder in poderes]
            poder_actual = personaje.poder
            nuevo_poder = simpledialog.askstring("Modificar Poder", f"Poder actual de {personaje.Nombre_Personaje}: {poder_actual.Nombre_Poder if poder_actual else 'Ninguno'}\nSelecciona el nuevo poder:", initialvalue=poder_actual.Nombre_Poder if poder_actual else None)
            if nuevo_poder in opciones:
                personaje.agregar_poder(next(poder for poder in poderes if poder.Nombre_Poder == nuevo_poder))
                personaje.save()

    def modificar_equipamiento(self):
        personaje = self.obtener_personaje_seleccionado()
        if personaje:
            ModificadorEquipamiento(self, personaje)

class ModificadorHabilidades(tk.Toplevel):
    def __init__(self, master, personaje):
        super().__init__(master)
        self.personaje = personaje
        self.title(f"Modificar Habilidades de {personaje.Nombre_Personaje}")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Habilidades disponibles:").pack(pady=(10, 5))
        self.habilidades_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=50, height=10)
        self.habilidades_listbox.pack(pady=5)
        self.cargar_habilidades()

        ttk.Button(self, text="Guardar cambios", command=self.guardar_cambios).pack(pady=10)

    def cargar_habilidades(self):
        habilidades = Habilidad.get_by_raza(self.personaje.ID_Raza)
        habilidades_personaje = Habilidad.get_by_personaje(self.personaje.ID_Personaje)
        for i, habilidad in enumerate(habilidades):
            self.habilidades_listbox.insert(tk.END, habilidad.Nombre_Habilidad)
            if habilidad in habilidades_personaje:
                self.habilidades_listbox.selection_set(i)

    def guardar_cambios(self):
        seleccion = self.habilidades_listbox.curselection()
        nuevas_habilidades = [Habilidad.get_by_raza(self.personaje.ID_Raza)[i] for i in seleccion]
        self.personaje.habilidades = nuevas_habilidades
        self.personaje.save()
        self.destroy()

class ModificadorEquipamiento(tk.Toplevel):
    def __init__(self, master, personaje):
        super().__init__(master)
        self.personaje = personaje
        self.title(f"Modificar Equipamiento de {personaje.Nombre_Personaje}")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Equipamiento disponible:").pack(pady=(10, 5))
        self.equipamiento_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=50, height=10)
        self.equipamiento_listbox.pack(pady=5)
        self.cargar_equipamiento()

        ttk.Button(self, text="Guardar cambios", command=self.guardar_cambios).pack(pady=10)

    def cargar_equipamiento(self):
        equipamiento = Equipamiento.get_all()
        equipamiento_personaje = Equipamiento.get_by_personaje(self.personaje.ID_Personaje)
        for i, equipo in enumerate(equipamiento):
            self.equipamiento_listbox.insert(tk.END, equipo.Nombre_Equipamiento)
            if equipo in equipamiento_personaje:
                self.equipamiento_listbox.selection_set(i)

    def guardar_cambios(self):
        seleccion = self.equipamiento_listbox.curselection()
        nuevo_equipamiento = [Equipamiento.get_all()[i] for i in seleccion]
        self.personaje.equipamiento = nuevo_equipamiento
        self.personaje.save()
        self.destroy()
        
class DetallesPersonaje(tk.Toplevel):
    def __init__(self, master, personaje):
        super().__init__(master)
        self.personaje = personaje
        self.title(f"Detalles de {personaje.Nombre_Personaje}")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text=f"Nombre: {self.personaje.Nombre_Personaje}").pack(pady=5)
        ttk.Label(self, text=f"Nivel: {self.personaje.Nivel}").pack(pady=5)
        raza = Raza.get_by_id(self.personaje.ID_Raza)
        ttk.Label(self, text=f"Raza: {raza.Nombre_Raza}").pack(pady=5)
        
        ttk.Label(self, text="Habilidades:").pack(pady=5)
        for habilidad in self.personaje.habilidades:
            ttk.Label(self, text=f"- {habilidad.Nombre_Habilidad}").pack()
        
        if self.personaje.poder:
            ttk.Label(self, text=f"Poder: {self.personaje.poder[0].Nombre_Poder if self.personaje.poder else 'Ninguno'}").pack(pady=5)
        
        ttk.Label(self, text="Equipamiento:").pack(pady=5)
        equipamiento = Personaje_Equipamiento.get_by_personaje(self.personaje.ID_Personaje)
        for equipo in equipamiento:
            equipo_detalle = Equipamiento.get_by_id(equipo.ID_Equipamiento)
            if equipo_detalle:
                ttk.Label(self, text=f"- {equipo_detalle.Nombre_Equipamiento}").pack()
        
        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)