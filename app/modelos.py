class Usuario:
    def __init__(self, id_usuario, nombre, usuario, contrasena):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena

class Personaje:
    def __init__(self, id_personaje, id_usuario, nombre_personaje, id_raza, nivel, id_estado):
        self.id_personaje = id_personaje
        self.id_usuario = id_usuario
        self.nombre_personaje = nombre_personaje
        self.id_raza = id_raza
        self.nivel = nivel
        self.id_estado = id_estado

class Equipamiento:
    def __init__(self, id_equipamiento, nombre_equipamiento, descripcion_equipamiento):
        self.id_equipamiento = id_equipamiento
        self.nombre_equipamiento = nombre_equipamiento
        self.descripcion_equipamiento = descripcion_equipamiento

class Estado:
    def __init__(self, id_estado, nombre_estado, descripcion_estado):
        self.id_estado = id_estado
        self.nombre_estado = nombre_estado
        self.descripcion_estado = descripcion_estado

class Raza:
    def __init__(self, id_raza, nombre_raza, descripcion_raza):
        self.id_raza = id_raza
        self.nombre_raza = nombre_raza
        self.descripcion_raza = descripcion_raza

class Habilidad:
    def __init__(self, id_habilidad, nombre_habilidad, descripcion_habilidad, id_raza):
        self.id_habilidad = id_habilidad
        self.nombre_habilidad = nombre_habilidad
        self.descripcion_habilidad = descripcion_habilidad
        self.id_raza = id_raza

class Poder:
    def __init__(self, id_poder, nombre_poder, descripcion_poder, id_raza):
        self.id_poder = id_poder
        self.nombre_poder = nombre_poder
        self.descripcion_poder = descripcion_poder
        self.id_raza = id_raza
