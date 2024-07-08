from database import Database
import hashlib

class Usuario:
    def __init__(self, ID_Usuario=None, Nombre=None, Usuario=None, Contrasena=None, Es_GM=False):
        self.ID_Usuario = ID_Usuario
        self.Nombre = Nombre
        self.Usuario = Usuario
        self.Contrasena = Contrasena
        self.Es_GM = Es_GM


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
                SET Nombre = %s, Usuario = %s, Contrasena = %s, Es_GM = %s 
                WHERE ID_Usuario = %s
                """
                db.execute_query(query, (self.Nombre, self.Usuario, self._hash_password(self.Contrasena), self.Es_GM, self.ID_Usuario))
            else:
                # Insertar
                query = """
                INSERT INTO usuario (Nombre, Usuario, Contrasena, Es_GM) 
                VALUES (%s, %s, %s, %s)
                """
                db.execute_query(query, (self.Nombre, self.Usuario, self._hash_password(self.Contrasena), self.Es_GM))
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

    @staticmethod
    def verificar_credenciales(usuario, contrasena):
        try:
            db = Database()
            hashed_password = Usuario._hash_password(contrasena)
            query = "SELECT * FROM usuario WHERE Usuario = %s AND Contrasena = %s"
            result = db.fetch_one(query, (usuario, hashed_password))
            if result:
                return Usuario(**result)
            return None

        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return None


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
    def get_all():
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM personaje")
            return [Personaje(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener todos los personajes: {e}")
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

    def asignar_habilidad(self, id_habilidad):
        try:
            db = Database()
            query = "INSERT INTO personaje_habilidad (ID_Personaje, ID_Habilidad) VALUES (%s, %s)"
            db.execute_query(query, (self.ID_Personaje, id_habilidad))
        except Exception as e:
            print(f"Error al asignar habilidad: {e}")

    def asignar_poder(self, id_poder):
        try:
            db = Database()
            query = "INSERT INTO personaje_poder (ID_Personaje, ID_Poder) VALUES (%s, %s)"
            db.execute_query(query, (self.ID_Personaje, id_poder))
        except Exception as e:
            print(f"Error al asignar poder: {e}")

    def get_habilidades(self):
        try:
            db = Database()
            query = """
            SELECT h.* FROM habilidad h
            JOIN personaje_habilidad ph ON h.ID_Habilidad = ph.ID_Habilidad
            WHERE ph.ID_Personaje = %s
            """
            results = db.fetch_all(query, (self.ID_Personaje,))
            return [Habilidad(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener habilidades del personaje: {e}")
            return []

    def get_poderes(self):
        try:
            db = Database()
            query = """
            SELECT p.* FROM poder p
            JOIN personaje_poder pp ON p.ID_Poder = pp.ID_Poder
            WHERE pp.ID_Personaje = %s
            """
            results = db.fetch_all(query, (self.ID_Personaje,))
            return [Poder(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener poderes del personaje: {e}")
            return []

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

class Habilidad:
    def __init__(self, ID_Habilidad=None, Nombre_Habilidad=None, Descripcion_Habilidad=None, ID_Raza=None):
        self.ID_Habilidad = ID_Habilidad
        self.Nombre_Habilidad = Nombre_Habilidad
        self.Descripcion_Habilidad = Descripcion_Habilidad
        self.ID_Raza = ID_Raza

    @staticmethod
    def get_by_raza(id_raza):
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM habilidad WHERE ID_Raza = %s", (id_raza,))
            return [Habilidad(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener habilidades por raza: {e}")
            return []

class Poder:
    def __init__(self, ID_Poder=None, Nombre_Poder=None, Descripcion_Poder=None, ID_Raza=None):
        self.ID_Poder = ID_Poder
        self.Nombre_Poder = Nombre_Poder
        self.Descripcion_Poder = Descripcion_Poder
        self.ID_Raza = ID_Raza

    @staticmethod
    def get_by_raza(id_raza):
        try:
            db = Database()
            results = db.fetch_all("SELECT * FROM poder WHERE ID_Raza = %s", (id_raza,))
            return [Poder(**result) for result in results]
        except Exception as e:
            print(f"Error al obtener poderes por raza: {e}")
            return []
