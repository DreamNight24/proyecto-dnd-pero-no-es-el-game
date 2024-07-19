import pymysql

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='juegoderol',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Conexión exitosa a la base de datos")
        except pymysql.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def ensure_connection(self):
        if not self.connection or not self.connection.open:
            self.connect()

    def test_connection(self):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    print("Conexión a la base de datos probada con éxito")
                else:
                    print("La prueba de conexión falló")
        except pymysql.Error as e:
            print(f"Error al probar la conexión: {e}")

    def execute_query(self, query, params=None):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                if query.strip().upper().startswith("INSERT"):
                    return cursor.lastrowid
                return cursor.rowcount
        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()
            raise

    def fetch_all(self, query, params=None):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error al obtener datos: {e}")
            raise

    def fetch_one(self, query, params=None):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error al obtener dato: {e}")
            raise

    def __del__(self):
        if self.connection and self.connection.open:
            self.connection.close()
            print("Conexión a la base de datos cerrada")

# Prueba de conexión
if __name__ == "__main__":
    try:
        db = Database()
        db.test_connection()
    except Exception as e:
        print(f"Error en la prueba principal: {e}")