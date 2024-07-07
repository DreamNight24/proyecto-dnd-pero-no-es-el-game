from database import Database
import hashlib

class Usuario:
    def __init__(self, ID_Usuario=None, Nombre=None, Usuario=None, Contrasena=None):
        self.ID_Usuario = ID_Usuario
        self.Nombre = Nombre
        self.Usuario = Usuario
        self.Contrasena = Contrasena

    @staticmethod
    def get_by_id(id_usuario):
        try:
            db = Database()
            result = db.fetch_one("SELECT * FROM usuario WHERE ID_Usuario = %s", (id_usuario,))
            if result:
                return Usuario(**result)
            return None
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM usuario")
            return [Usuario(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []

    def save(self):
        try:
            db = Database()
            if self.ID_Usuario:
                # Actualizar
                query = """
                UPDATE usuario 
                SET Nombre = %s, Usuario = %s, Contrasena = %s 
                WHERE ID_Usuario = %s
                """
                db.execute_query(query, (self.Nombre, self.Usuario, self._hash_password(self.Contrasena), self.ID_Usuario))
            else:
                # Insertar
                query = """
                INSERT INTO usuario (Nombre, Usuario, Contrasena) 
                VALUES (%s, %s, %s)
                """
                db.execute_query(query, (self.Nombre, self.Usuario, self._hash_password(self.Contrasena)))
        except Exception as e:
            print(f"Error al guardar usuario: {e}")

    def delete(self):
        if not self.ID_Usuario:
            raise ValueError("Cannot delete a user without an ID")
        try:
            db = Database()
            query = "DELETE FROM usuario WHERE ID_Usuario = %s"
            db.execute_query(query, (self.ID_Usuario,))
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

class Personaje:
    def __init__(self, ID_Personaje=None, ID_Usuario=None, Nombre_Personaje=None, ID_Raza=None, Nivel=1, ID_Estado=None):
        self.ID_Personaje = ID_Personaje
        self.ID_Usuario = ID_Usuario
        self.Nombre_Personaje = Nombre_Personaje
        self.ID_Raza = ID_Raza
        self.Nivel = Nivel
        self.ID_Estado = ID_Estado

    @staticmethod
    def get_by_id(id_personaje):
        try:
            db = Database()
            result = db.fetch_one("SELECT * FROM personaje WHERE ID_Personaje = %s", (id_personaje,))
            if result:
                return Personaje(**result)
            return None
        except Exception as e:
            print(f"Error al obtener personaje por ID: {e}")
            return None

    @staticmethod
    def get_all_by_user(id_usuario):
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM personaje WHERE ID_Usuario = %s", (id_usuario,))
            return [Personaje(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener personajes del usuario: {e}")
            return []

    def save(self):
        try:
            db = Database()
            if self.ID_Personaje:
                # Actualizar
                query = """
                UPDATE personaje 
                SET ID_Usuario = %s, Nombre_Personaje = %s, ID_Raza = %s, Nivel = %s, ID_Estado = %s 
                WHERE ID_Personaje = %s
                """
                db.execute_query(query, (self.ID_Usuario, self.Nombre_Personaje, self.ID_Raza, self.Nivel, self.ID_Estado, self.ID_Personaje))
            else:
                # Insertar
                query = """
                INSERT INTO personaje (ID_Usuario, Nombre_Personaje, ID_Raza, Nivel, ID_Estado) 
                VALUES (%s, %s, %s, %s, %s)
                """
                db.execute_query(query, (self.ID_Usuario, self.Nombre_Personaje, self.ID_Raza, self.Nivel, self.ID_Estado))
        except Exception as e:
            print(f"Error al guardar personaje: {e}")

class Raza:
    def __init__(self, ID_Raza=None, Nombre_Raza=None, Descripcion_Raza=None):
        self.ID_Raza = ID_Raza
        self.Nombre_Raza = Nombre_Raza
        self.Descripcion_Raza = Descripcion_Raza

    @staticmethod
    def get_all():
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM raza")
            return [Raza(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener todas las razas: {e}")
            return []

    @staticmethod
    def get_by_id(id_raza):
        try:
            db = Database()
            result = db.fetch_one("SELECT * FROM raza WHERE ID_Raza = %s", (id_raza,))
            if result:
                return Raza(**result)
            return None
        except Exception as e:
            print(f"Error al obtener raza por ID: {e}")
            return None

class Estado:
    def __init__(self, ID_Estado=None, Nombre_Estado=None, Descripcion_Estado=None):
        self.ID_Estado = ID_Estado
        self.Nombre_Estado = Nombre_Estado
        self.Descripcion_Estado = Descripcion_Estado

    @staticmethod
    def get_all():
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM estado")
            return [Estado(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener todos los estados: {e}")
            return []

    @staticmethod
    def get_by_id(id_estado):
        try:
            db = Database()
            result = db.fetch_one("SELECT * FROM estado WHERE ID_Estado = %s", (id_estado,))
            if result:
                return Estado(**result)
            return None
        except Exception as e:
            print(f"Error al obtener estado por ID: {e}")
            return None