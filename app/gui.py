import tkinter as tk
from tkinter import ttk, messagebox
from models import Usuario, Personaje, Raza, Estado, Habilidad, Poder

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Juego de Rol")
        self.pack()
        self.usuario_actual = None
        self.es_gm = False
        self.create_widgets()

    def create_widgets(self): # crear cajas interactivas
        self.login_button = ttk.Button(self, text="Iniciar Sesión", command=self.login)
        self.login_button.pack()

        self.usuario_mantenedor_button = ttk.Button(self, text="Mantenedor de Usuarios", command=self.abrir_usuario_mantenedor)
        self.usuario_mantenedor_button.pack()

        self.crear_personaje_button = ttk.Button(self, text="Crear Personaje", command=self.abrir_creador_personaje, state="disabled")
        self.crear_personaje_button.pack()

        self.mostrar_personajes_button = ttk.Button(self, text="Mostrar Personajes", command=self.mostrar_personajes, state="disabled")
        self.mostrar_personajes_button.pack()

        self.modificar_personaje_button = ttk.Button(self, text="Modificar Personaje (GM)", command=self.abrir_modificador_personaje, state="disabled")
        self.modificar_personaje_button.pack()

    def login(self): # se crea el sistema de login
        login_window = tk.Toplevel(self.master)
        login_window.title("Iniciar Sesión")

        ttk.Label(login_window, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        usuario_entry = ttk.Entry(login_window)
        usuario_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_window, text="Contraseña:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        contrasena_entry = ttk.Entry(login_window, show="*")
        contrasena_entry.grid(row=1, column=1, padx=5, pady=5)

        def verificar_login(): # se verifica el login del usuario
            usuario = usuario_entry.get()
            contrasena = contrasena_entry.get()

            usuario_obj = Usuario.verificar_credenciales(usuario, contrasena)
            if usuario_obj:
                self.usuario_actual = usuario_obj.ID_Usuario
                self.es_gm = usuario_obj.Es_GM
                self.crear_personaje_button['state'] = 'normal'
                self.mostrar_personajes_button['state'] = 'normal'
                if self.es_gm:
                    self.modificar_personaje_button['state'] = 'normal'
                login_window.destroy()
                messagebox.showinfo("Éxito", f"Bienvenido, {usuario_obj.Nombre}!")
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")

        ttk.Button(login_window, text="Iniciar Sesión", command=verificar_login).grid(row=2, column=0, columnspan=2, pady=10)


    def abrir_usuario_mantenedor(self): # abre el mantenedor de usuario
        UsuarioMantenedor(self.master)

    def abrir_creador_personaje(self): # abre el creador de personaje 
        if self.usuario_actual:
            CreadorPersonaje(self.master, self.usuario_actual)
        else:
            messagebox.showerror("Error", "Debe iniciar sesión primero")

    def mostrar_personajes(self): # muestra personajes
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debe iniciar sesión primero")
            return

        personajes = Personaje.get_all_by_user(self.usuario_actual) # obtiene todos los personajes del usuario
        if not personajes:
            messagebox.showinfo("Información", "No tienes personajes creados")
            return

        reporte = "Tus personajes:\n\n" # reporte de los personajes del usuario.
        for personaje in personajes:
            raza = Raza.get_by_id(personaje.ID_Raza)
            estado = Estado.get_by_id(personaje.ID_Estado)
            reporte += f"Nombre: {personaje.Nombre_Personaje}\n"
            reporte += f"Raza: {raza.Nombre_Raza if raza else 'Desconocida'}\n"
            reporte += f"Nivel: {personaje.Nivel}\n"
            reporte += f"Estado: {estado.Nombre_Estado if estado else 'Desconocido'}\n\n"

        messagebox.showinfo("Reporte de Personajes", reporte)

    def abrir_modificador_personaje(self): # abre el modificador de los personajes para el GM
        if self.es_gm:
            GMModificadorPersonaje(self.master)
        else:
            messagebox.showerror("Error", "Solo los GM pueden modificar personajes")        

class UsuarioMantenedor(tk.Toplevel): # la clase que mantiene usuarios, hence the name
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Mantenedor de Usuarios")
        self.create_widgets()

    def create_widgets(self): # crea los botones para crear, leer, actualizar y eliminar usuario.
        # Campos de entrada
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.grid(row=0, column=1)

        ttk.Label(self, text="Usuario:").grid(row=1, column=0, sticky="w")
        self.usuario_entry = ttk.Entry(self)
        self.usuario_entry.grid(row=1, column=1)

        ttk.Label(self, text="Contraseña:").grid(row=2, column=0, sticky="w")
        self.contrasena_entry = ttk.Entry(self, show="*")
        self.contrasena_entry.grid(row=2, column=1)

        ttk.Label(self, text="Es GM:").grid(row=3, column=0, sticky="w")
        self.es_gm_var = tk.BooleanVar()
        self.es_gm_checkbox = ttk.Checkbutton(self, variable=self.es_gm_var)
        self.es_gm_checkbox.grid(row=3, column=1)

        # Botones CRUD
        ttk.Button(self, text="Crear", command=self.crear_usuario).grid(row=4, column=0)
        ttk.Button(self, text="Leer", command=self.leer_usuarios).grid(row=4, column=1)
        ttk.Button(self, text="Actualizar", command=self.actualizar_usuario).grid(row=5, column=0)
        ttk.Button(self, text="Eliminar", command=self.eliminar_usuario).grid(row=5, column=1)

        # Lista de usuarios
        self.usuarios_listbox = tk.Listbox(self)
        self.usuarios_listbox.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # Cargar usuarios al abrir el mantenedor
        self.leer_usuarios()

    def crear_usuario(self):
        nombre = self.nombre_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get()
        es_gm = self.es_gm_var.get()

        if not nombre or not usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if len(contrasena) < 8:
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres")
            return

        nuevo_usuario = Usuario(Nombre=nombre, Usuario=usuario, Contrasena=contrasena, Es_GM=es_gm)
        nuevo_usuario.save()
        messagebox.showinfo("Éxito", "Usuario creado correctamente")
        self.leer_usuarios()

    def leer_usuarios(self):
        self.usuarios_listbox.delete(0, tk.END)
        usuarios = Usuario.get_all()
        for usuario in usuarios:
            self.usuarios_listbox.insert(tk.END, f"{usuario.ID_Usuario}: {usuario.Nombre} ({usuario.Usuario})")

    def actualizar_usuario(self):
        seleccion = self.usuarios_listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para actualizar")
            return

        id_usuario = int(self.usuarios_listbox.get(seleccion[0]).split(':')[0])
        usuario = Usuario.get_by_id(id_usuario)
        if usuario:
            usuario.Nombre = self.nombre_entry.get().strip()
            usuario.Usuario = self.usuario_entry.get().strip()
            nueva_contrasena = self.contrasena_entry.get()
            if nueva_contrasena:
                usuario.Contrasena = nueva_contrasena
            usuario.save()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            self.leer_usuarios()

    def eliminar_usuario(self):
        seleccion = self.usuarios_listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para eliminar")
            return

        id_usuario = int(self.usuarios_listbox.get(seleccion[0]).split(':')[0])
        usuario = Usuario.get_by_id(id_usuario)
        if usuario:
            usuario.delete()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            self.leer_usuarios()

class CreadorPersonaje(tk.Toplevel):
    def __init__(self, master=None, id_usuario=None):
        super().__init__(master)
        self.id_usuario = id_usuario
        self.title("Crear Personaje")
        self.habilidades_seleccionadas = []
        self.poder_seleccionado = None
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Nombre del Personaje:").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.grid(row=0, column=1)

        ttk.Label(self, text="Raza:").grid(row=1, column=0, sticky="w")
        self.raza_combobox = ttk.Combobox(self, state="readonly")
        self.raza_combobox.grid(row=1, column=1)

        ttk.Label(self, text="Habilidades:").grid(row=2, column=0, sticky="w")
        self.habilidades_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.habilidades_listbox.grid(row=2, column=1)

        ttk.Label(self, text="Poder:").grid(row=3, column=0, sticky="w")
        self.poder_combobox = ttk.Combobox(self, state="readonly")
        self.poder_combobox.grid(row=3, column=1)

        ttk.Button(self, text="Crear Personaje", command=self.crear_personaje).grid(row=4, column=0, columnspan=2)

        self.cargar_razas()

    def cargar_razas(self):
        razas = Raza.get_all()
        self.raza_combobox['values'] = [raza.Nombre_Raza for raza in razas]
        if razas:
            self.raza_combobox.current(0)
        self.raza_combobox.bind("<<ComboboxSelected>>", self.actualizar_habilidades_y_poderes)

    def actualizar_habilidades_y_poderes(self, event=None):
        raza = self.raza_combobox.get()
        razas = Raza.get_all()
        id_raza = next((r.ID_Raza for r in razas if r.Nombre_Raza == raza), None)

        if id_raza is None:
            return

        habilidades = Habilidad.get_by_raza(id_raza)
        self.habilidades_listbox.delete(0, tk.END)
        for habilidad in habilidades:
            self.habilidades_listbox.insert(tk.END, habilidad.Nombre_Habilidad)

        poderes = Poder.get_by_raza(id_raza)
        self.poder_combobox['values'] = [poder.Nombre_Poder for poder in poderes]
        if poderes:
            self.poder_combobox.current(0)

    def crear_personaje(self):
        nombre = self.nombre_entry.get().strip()
        raza = self.raza_combobox.get()
        habilidades_indices = self.habilidades_listbox.curselection()
        poder = self.poder_combobox.get()

        if not nombre or not raza or len(habilidades_indices) != 2 or not poder:
            messagebox.showerror("Error", "Debe seleccionar un nombre, una raza, exactamente 2 habilidades y un poder")
            return

        razas = Raza.get_all()
        id_raza = next((r.ID_Raza for r in razas if r.Nombre_Raza == raza), None)

        if id_raza is None:
            messagebox.showerror("Error", "Raza no válida")
            return

        estados = Estado.get_all()
        id_estado_vivo = next((e.ID_Estado for e in estados if e.Nombre_Estado == "Vivo"), None)

        if id_estado_vivo is None:
            messagebox.showerror("Error", "No se pudo encontrar el estado 'Vivo'")
            return

        nuevo_personaje = Personaje(
            ID_Usuario=self.id_usuario,
            Nombre_Personaje=nombre,
            ID_Raza=id_raza,
            Nivel=1,
            ID_Estado=id_estado_vivo
        )
        nuevo_personaje.save()

        habilidades = Habilidad.get_by_raza(id_raza)
        for indice in habilidades_indices:
            nuevo_personaje.asignar_habilidad(habilidades[indice].ID_Habilidad)

        poderes = Poder.get_by_raza(id_raza)
        id_poder = next((p.ID_Poder for p in poderes if p.Nombre_Poder == poder), None)
        if id_poder:
            nuevo_personaje.asignar_poder(id_poder)

        messagebox.showinfo("Éxito", "Personaje creado correctamente")
        self.destroy()

class GMModificadorPersonaje(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Modificar Personaje (GM)")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Seleccionar Personaje:").grid(row=0, column=0, sticky="w")
        self.personaje_combobox = ttk.Combobox(self, state="readonly")
        self.personaje_combobox.grid(row=0, column=1)
        self.cargar_personajes()

        ttk.Label(self, text="Nivel:").grid(row=1, column=0, sticky="w")
        self.nivel_entry = ttk.Entry(self)
        self.nivel_entry.grid(row=1, column=1)

        ttk.Label(self, text="Estado:").grid(row=2, column=0, sticky="w")
        self.estado_combobox = ttk.Combobox(self, state="readonly")
        self.estado_combobox.grid(row=2, column=1)
        self.cargar_estados()

        ttk.Label(self, text="Habilidades:").grid(row=3, column=0, sticky="w")
        self.habilidades_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.habilidades_listbox.grid(row=3, column=1)

        ttk.Label(self, text="Poderes:").grid(row=4, column=0, sticky="w")
        self.poderes_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.poderes_listbox.grid(row=4, column=1)

        ttk.Button(self, text="Guardar Cambios", command=self.guardar_cambios).grid(row=5, column=0, columnspan=2)

        self.personaje_combobox.bind("<<ComboboxSelected>>", self.cargar_datos_personaje)

    def cargar_personajes(self):
        personajes = Personaje.get_all()
        self.personaje_combobox['values'] = [f"{p.ID_Personaje}: {p.Nombre_Personaje}" for p in personajes]

    def cargar_estados(self):
        estados = Estado.get_all()
        self.estado_combobox['values'] = [estado.Nombre_Estado for estado in estados]

    def cargar_datos_personaje(self, event=None):
        personaje_id = int(self.personaje_combobox.get().split(':')[0])
        personaje = Personaje.get_by_id(personaje_id)
        if personaje:
            self.nivel_entry.delete(0, tk.END)
            self.nivel_entry.insert(0, str(personaje.Nivel))
            
            estado = Estado.get_by_id(personaje.ID_Estado)
            if estado:
                self.estado_combobox.set(estado.Nombre_Estado)

            self.cargar_habilidades_y_poderes(personaje)

    def cargar_habilidades_y_poderes(self, personaje):
        self.habilidades_listbox.delete(0, tk.END)
        self.poderes_listbox.delete(0, tk.END)

        habilidades_personaje = personaje.get_habilidades()
        poderes_personaje = personaje.get_poderes()

        todas_habilidades = Habilidad.get_by_raza(personaje.ID_Raza)
        todos_poderes = Poder.get_by_raza(personaje.ID_Raza)

        for habilidad in todas_habilidades:
            self.habilidades_listbox.insert(tk.END, habilidad.Nombre_Habilidad)
            if habilidad in habilidades_personaje:
                self.habilidades_listbox.selection_set(tk.END)

        for poder in todos_poderes:
            self.poderes_listbox.insert(tk.END, poder.Nombre_Poder)
            if poder in poderes_personaje:
                self.poderes_listbox.selection_set(tk.END)

    def guardar_cambios(self):
        personaje_id = int(self.personaje_combobox.get().split(':')[0])
        personaje = Personaje.get_by_id(personaje_id)
        if not personaje:
            messagebox.showerror("Error", "Personaje no encontrado")
            return

        # Actualizar nivel
        nuevo_nivel = int(self.nivel_entry.get())
        if nuevo_nivel > personaje.Nivel:
            personaje.Nivel = nuevo_nivel
        
        # Actualizar estado
        nuevo_estado = Estado.get_by_name(self.estado_combobox.get())
        if nuevo_estado:
            personaje.ID_Estado = nuevo_estado.ID_Estado

        # Actualizar habilidades y poderes
        nuevas_habilidades = [Habilidad.get_by_name(self.habilidades_listbox.get(idx)) 
        for idx in self.habilidades_listbox.curselection()]
        nuevos_poderes = [Poder.get_by_name(self.poderes_listbox.get(idx)) 
        for idx in self.poderes_listbox.curselection()]

        personaje.actualizar_habilidades(nuevas_habilidades)
        personaje.actualizar_poderes(nuevos_poderes)

        personaje.save()
        messagebox.showinfo("Éxito", "Personaje actualizado correctamente")