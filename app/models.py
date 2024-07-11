from database import Database
import hashlib

class Usuario:
    def __init__(self, ID_Usuario=None, Nombre=None, Usuario=None, Contrasena=None, Es_GM=False):
        self.ID_Usuario = ID_Usuario
        self.Nombre = Nombre
        self.Usuario = Usuario
        self.Contrasena = Contrasena
        self.Es_GM = Es_GM

    @property
    def es_gm(self):
        return self.Es_GM

    @staticmethod
    def get_by_id(id_usuario):
        db = Database()
        result = db.fetch_one("SELECT * FROM usuario WHERE ID_Usuario = %s", (id_usuario,))
        if result:
            return Usuario(**result)
        return None

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM usuario")
        return [Usuario(**result) for result in results]

    def save(self):
        db = Database()
        if self.ID_Usuario:
            query = """
            UPDATE usuario
            SET Nombre = %s, Usuario = %s, Contrasena = %s, Es_GM = %s
            WHERE ID_Usuario = %s
            """
            db.execute_query(query, (self.Nombre, self.Usuario, self._hash_password(self.Contrasena), self.Es_GM, self.ID_Usuario))
        else:
            query = """
            INSERT INTO usuario (Nombre, Usuario, Contrasena, Es_GM)
            VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, (self.Nombre, self.Usuario, self._hash_password(self.Contrasena), self.Es_GM))

    def delete(self):
        if not self.ID_Usuario:
            raise ValueError("Cannot delete a user without an ID")
        db = Database()
        query = "DELETE FROM usuario WHERE ID_Usuario = %s"
        db.execute_query(query, (self.ID_Usuario,))

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verificar_credenciales(usuario, contrasena):
        db = Database()
        hashed_password = Usuario._hash_password(contrasena)
        query = "SELECT * FROM usuario WHERE Usuario = %s AND Contrasena = %s"
        result = db.fetch_one(query, (usuario, hashed_password))
        if result:
            return Usuario(**result)
        return None

class Personaje:
    def __init__(self, ID_Personaje=None, ID_Usuario=None, Nombre_Personaje=None, ID_Raza=None, Nivel=1, ID_Estado=None, ID_Equipamiento=None, ID_Poder=None):
        self.ID_Personaje = ID_Personaje
        self.ID_Usuario = ID_Usuario
        self.Nombre_Personaje = Nombre_Personaje
        self.ID_Raza = ID_Raza
        self.Nivel = Nivel
        self.ID_Estado = ID_Estado
        self.ID_Equipamiento = ID_Equipamiento
        self.ID_Poder = ID_Poder
        self.habilidades = []
        self.poder = None

    @staticmethod
    def get_by_id(id_personaje):
        db = Database()
        result = db.fetch_one("SELECT * FROM personaje WHERE ID_Personaje = %s", (id_personaje,))
        if result:
            personaje = Personaje(**result)
            personaje.cargar_habilidades()
            personaje.cargar_poder()
            return personaje
        return None

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM personaje")
        personajes = []
        for result in results:
            personaje = Personaje(**result)
            personaje.cargar_habilidades()
            personaje.cargar_poder()
            personajes.append(personaje)
        return personajes

    def save(self):
        db = Database()
        if self.ID_Personaje:
            query = """
            UPDATE personaje
            SET ID_Usuario = %s, Nombre_Personaje = %s, ID_Raza = %s, Nivel = %s, ID_Estado = %s
            WHERE ID_Personaje = %s
            """
            db.execute_query(query, (self.ID_Usuario, self.Nombre_Personaje, self.ID_Raza, self.Nivel, self.ID_Estado, self.ID_Personaje))
        else:
            query = """
            INSERT INTO personaje (ID_Usuario, Nombre_Personaje, ID_Raza, Nivel, ID_Estado)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.ID_Personaje = db.execute_query(query, (self.ID_Usuario, self.Nombre_Personaje, self.ID_Raza, self.Nivel, self.ID_Estado))
        self.save_habilidades()
        self.save_poder()
        self.save_equipamiento()

    def save_habilidades(self):
        db = Database()
        db.execute_query("DELETE FROM personaje_habilidad WHERE ID_Personaje = %s", (self.ID_Personaje,))
        for habilidad in self.habilidades:
            db.execute_query("INSERT INTO personaje_habilidad (ID_Personaje, ID_Habilidad) VALUES (%s, %s)",
                             (self.ID_Personaje, habilidad.ID_Habilidad))
    def save_poder(self):
        db = Database()
        if self.poder and isinstance(self.poder, list) and len(self.poder) > 0:
           db.execute_query("UPDATE personaje SET ID_Poder = %s WHERE ID_Personaje = %s", (self.poder[0].ID_Poder, self.ID_Personaje))
        else:
           db.execute_query("UPDATE personaje SET ID_Poder = NULL WHERE ID_Personaje = %s", (self.ID_Personaje,))

    def cargar_habilidades(self):
        self.habilidades = Habilidad.get_by_raza(self.ID_Raza)
     
    def cargar_equipamiento(self):
        self.equipamiento = Personaje_Equipamiento.get_by_personaje(self.ID_Personaje)

    def cargar_poder(self):
        self.poder = Poder.get_by_raza(self.ID_Raza)

    def agregar_habilidad(self, habilidad):
        if habilidad not in self.habilidades:
            self.habilidades.append(habilidad)

    def eliminar_habilidad(self, habilidad):
        if habilidad in self.habilidades:
            self.habilidades.remove(habilidad)

    def agregar_poder(self, poder):
        self.poder = poder

    def eliminar_poder(self):
        self.poder = None

    @staticmethod
    def get_by_usuario(id_usuario):
        db = Database()
        results = db.fetch_all("SELECT * FROM personaje WHERE ID_Usuario = %s", (id_usuario,))
        personajes = []
        for result in results:
            personaje = Personaje(**result)
            personaje.cargar_habilidades()
            personaje.cargar_poder()
            personajes.append(personaje)
        return personajes



class Raza:
    def __init__(self, ID_Raza=None, Nombre_Raza=None, Descripcion_Raza=None):
        self.ID_Raza = ID_Raza
        self.Nombre_Raza = Nombre_Raza
        self.Descripcion_Raza = Descripcion_Raza

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM raza")
        return [Raza(**result) for result in results]

    @staticmethod
    def get_by_id(id_raza):
        db = Database()
        result = db.fetch_one("SELECT * FROM raza WHERE ID_Raza = %s", (id_raza,))
        if result:
            return Raza(**result)
        return None

    def save(self):
        db = Database()
        if self.ID_Raza:
            query = "UPDATE raza SET Nombre_Raza = %s, Descripcion_Raza = %s WHERE ID_Raza = %s"
            db.execute_query(query, (self.Nombre_Raza, self.Descripcion_Raza, self.ID_Raza))
        else:
            query = "INSERT INTO raza (Nombre_Raza, Descripcion_Raza) VALUES (%s, %s)"
            db.execute_query(query, (self.Nombre_Raza, self.Descripcion_Raza))

    def delete(self):
        if not self.ID_Raza:
            raise ValueError("Cannot delete a race without an ID")
        db = Database()
        query = "DELETE FROM raza WHERE ID_Raza = %s"
        db.execute_query(query, (self.ID_Raza,))

    @staticmethod
    def get_by_nombre(nombre_raza):
        db = Database()
        result = db.fetch_one("SELECT * FROM raza WHERE Nombre_Raza = %s", (nombre_raza,))
        if result:
            return Raza(**result)
        return None


class Estado:
    def __init__(self, ID_Estado=None, Nombre_Estado=None, Descripcion_Estado=None):
        self.ID_Estado = ID_Estado
        self.Nombre_Estado = Nombre_Estado
        self.Descripcion_Estado = Descripcion_Estado

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM estado")
        return [Estado(**result) for result in results]

    @staticmethod
    def get_by_id(id_estado):
        db = Database()
        result = db.fetch_one("SELECT * FROM estado WHERE ID_Estado = %s", (id_estado,))
        if result:
            return Estado(**result)
        return None

    def save(self):
        db = Database()
        if self.ID_Estado:
            query = "UPDATE estado SET Nombre_Estado = %s, Descripcion_Estado = %s WHERE ID_Estado = %s"
            db.execute_query(query, (self.Nombre_Estado, self.Descripcion_Estado, self.ID_Estado))
        else:
            query = "INSERT INTO estado (Nombre_Estado, Descripcion_Estado) VALUES (%s, %s)"
            db.execute_query(query, (self.Nombre_Estado, self.Descripcion_Estado))

class Habilidad:
    def __init__(self, ID_Habilidad=None, Nombre_Habilidad=None, Descripcion_Habilidad=None, ID_Raza=None):
        self.ID_Habilidad = ID_Habilidad
        self.Nombre_Habilidad = Nombre_Habilidad
        self.Descripcion_Habilidad = Descripcion_Habilidad
        self.ID_Raza = ID_Raza

    @staticmethod
    def get_by_raza(id_raza):
        db = Database()
        results = db.fetch_all("SELECT * FROM habilidad WHERE ID_Raza = %s", (id_raza,))
        return [Habilidad(**result) for result in results]

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM habilidad")
        return [Habilidad(**result) for result in results]

    def save(self):
        db = Database()
        if self.ID_Habilidad:
            query = """
            UPDATE habilidad
            SET Nombre_Habilidad = %s, Descripcion_Habilidad = %s, ID_Raza = %s
            WHERE ID_Habilidad = %s
            """
            db.execute_query(query, (self.Nombre_Habilidad, self.Descripcion_Habilidad, self.ID_Raza, self.ID_Habilidad))
        else:
            query = """
            INSERT INTO habilidad (Nombre_Habilidad, Descripcion_Habilidad, ID_Raza)
            VALUES (%s, %s, %s)
            """
            db.execute_query(query, (self.Nombre_Habilidad, self.Descripcion_Habilidad, self.ID_Raza))

    def delete(self):
        if not self.ID_Habilidad:
            raise ValueError("No se puede eliminar una habilidad sin ID")
        db = Database()
        query = "DELETE FROM habilidad WHERE ID_Habilidad = %s"
        db.execute_query(query, (self.ID_Habilidad,))

    @staticmethod
    def get_by_nombre(nombre_habilidad):
        db = Database()
        result = db.fetch_one("SELECT * FROM habilidad WHERE Nombre_Habilidad = %s", (nombre_habilidad,))
        if result:
            return Habilidad(**result)
            return None

    @staticmethod
    def get_by_personaje(id_personaje):
        db = Database()
        query = """
        SELECT h.* FROM habilidad h
        JOIN personaje_habilidad ph ON h.ID_Habilidad = ph.ID_Habilidad
        WHERE ph.ID_Personaje = %s
        """
        return db.fetch_all(query, (id_personaje,))

class Poder:
    def __init__(self, ID_Poder=None, Nombre_Poder=None, Descripcion_Poder=None, ID_Raza=None):
        self.ID_Poder = ID_Poder
        self.Nombre_Poder = Nombre_Poder
        self.Descripcion_Poder = Descripcion_Poder
        self.ID_Raza = ID_Raza

    @staticmethod
    def get_by_raza(id_raza):
        db = Database()
        results = db.fetch_all("SELECT * FROM poder WHERE ID_Raza = %s", (id_raza,))
        return [Poder(**result) for result in results]

    def save(self):
        db = Database()
        if self.ID_Poder:
            query = """
            UPDATE poder
            SET Nombre_Poder = %s, Descripcion_Poder = %s, ID_Raza = %s
            WHERE ID_Poder = %s
            """
            db.execute_query(query, (self.Nombre_Poder, self.Descripcion_Poder, self.ID_Raza, self.ID_Poder))
        else:
            query = """
            INSERT INTO poder (Nombre_Poder, Descripcion_Poder, ID_Raza)
            VALUES (%s, %s, %s)
            """
            db.execute_query(query, (self.Nombre_Poder, self.Descripcion_Poder, self.ID_Raza))

    @staticmethod
    def get_by_nombre(nombre_poder):
        db = Database()
        result = db.fetch_one("SELECT * FROM poder WHERE Nombre_Poder = %s", (nombre_poder,))
        if result:
            return Poder(**result)
        return None

    @staticmethod
    def get_by_personaje(id_personaje):
        db = Database()
        query = """
        SELECT p.* FROM poder p
        JOIN personaje_poder pp ON p.ID_Poder = pp.ID_Poder
        WHERE pp.ID_Personaje = %s
        """
        results = db.fetch_all(query, (id_personaje,))
        return [Poder(**result) for result in results] if results else None

class Equipamiento:
    def __init__(self, ID_Equipamiento=None, Nombre_Equipamiento=None, Descripcion_Equipamiento=None):
        self.ID_Equipamiento = ID_Equipamiento
        self.Nombre_Equipamiento = Nombre_Equipamiento
        self.Descripcion_Equipamiento = Descripcion_Equipamiento

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM equipamiento")
        return [Equipamiento(**result) for result in results]

    @staticmethod
    def get_by_id(id_equipamiento):
        db = Database()
        result = db.fetch_one("SELECT * FROM equipamiento WHERE ID_Equipamiento = %s", (id_equipamiento,))
        if result:
            return Equipamiento(**result)
        return None

    def save(self):
        db = Database()
        if self.ID_Equipamiento:
            query = """
            UPDATE equipamiento
            SET Nombre_Equipamiento = %s, Descripcion_Equipamiento = %s
            WHERE ID_Equipamiento = %s
            """
            db.execute_query(query, (self.Nombre_Equipamiento, self.Descripcion_Equipamiento, self.ID_Equipamiento))
        else:
            query = """
            INSERT INTO equipamiento (Nombre_Equipamiento, Descripcion_Equipamiento)
            VALUES (%s, %s)
            """
            db.execute_query(query, (self.Nombre_Equipamiento, self.Descripcion_Equipamiento))

    @staticmethod
    def get_by_nombre(nombre):
        db = Database()
        result = db.fetch_one("SELECT * FROM equipamiento WHERE Nombre_Equipamiento = %s", (nombre,))
        return Equipamiento(**result) if result else None

    def delete(self):
        db = Database()
        query = "DELETE FROM equipamiento WHERE ID_Equipamiento = %s"
        db.execute_query(query, (self.ID_Equipamiento,))

    @staticmethod
    def get_by_personaje(id_personaje):
     db = Database()
     query = """
     SELECT e.* FROM equipamiento e
     JOIN personaje_equipamiento pe ON e.ID_Equipamiento = pe.id_Equipamiento
     WHERE pe.id_personaje = %s
     """
     results = db.fetch_all(query, (id_personaje,))
     return [Equipamiento(**result) for result in results]

class Personaje_Equipamiento:
    def __init__(self, ID_Personaje=None, ID_Equipamiento=None):
        self.ID_Personaje = ID_Personaje
        self.ID_Equipamiento = ID_Equipamiento

    @staticmethod
    def get_by_personaje(id_personaje):
        db = Database()
        results = db.fetch_all("SELECT * FROM personaje_equipamiento WHERE ID_Personaje = %s", (id_personaje,))
        return [Personaje_Equipamiento(**result) for result in results]

    def save(self):
        db = Database()
        query = """
        INSERT INTO personaje_equipamiento (ID_Personaje, ID_Equipamiento)
        VALUES (%s, %s)
        """
        db.execute_query(query, (self.ID_Personaje, self.ID_Equipamiento))

    def delete(self):
        db = Database()
        query = "DELETE FROM personaje_equipamiento WHERE ID_Personaje = %s AND ID_Equipamiento = %s"
        db.execute_query(query, (self.ID_Personaje, self.ID_Equipamiento))

class Estado:
    def __init__(self, ID_Estado=None, Nombre_Estado=None):
        self.ID_Estado = ID_Estado
        self.Nombre_Estado = Nombre_Estado

    @staticmethod
    def get_all():
        db = Database()
        results = db.fetch_all("SELECT * FROM estado")
        return [Estado(**result) for result in results]

    @staticmethod
    def get_by_id(id_estado):
        db = Database()
        result = db.fetch_one("SELECT * FROM estado WHERE ID_Estado = %s", (id_estado,))
        if result:
            return Estado(**result)
        return None

    def save(self):
        db = Database()
        if self.ID_Estado:
            query = "UPDATE estado SET Nombre_Estado = %s WHERE ID_Estado = %s"
            db.execute_query(query, (self.Nombre_Estado, self.ID_Estado))
        else:
            query = "INSERT INTO estado (Nombre_Estado) VALUES (%s)"
            self.ID_Estado = db.execute_query(query, (self.Nombre_Estado,))

    def delete(self):
        if not self.ID_Estado:
            raise ValueError("Cannot delete a state without an ID")
        db = Database()
        query = "DELETE FROM estado WHERE ID_Estado = %s"
        db.execute_query(query, (self.ID_Estado,))