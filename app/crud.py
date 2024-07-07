from app.db import connect_to_db
from app.modelos import Usuario, Personaje, Equipamiento, Estado, Raza, Habilidad, Poder
import pymysql

def crear_usuario(nombre, usuario, contrasena):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO usuario (Nombre, Usuario, Contrasena) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, usuario, contrasena))
        connection.commit()
    finally:
        connection.close()

def obtener_usuarios():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuario"
            cursor.execute(sql)
            result = cursor.fetchall()
            return [Usuario(**user) for user in result]
    finally:
        connection.close()

def usuario_existe(id_usuario):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT ID_Usuario FROM usuario WHERE ID_Usuario = %s"
            cursor.execute(sql, (id_usuario,))
            result = cursor.fetchone()
            return result is not None
    finally:
        connection.close()


def crear_personaje(id_usuario, nombre_personaje, id_raza, id_estado, id_equipamiento=1):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO personaje (ID_Usuario, Nombre_Personajes, ID_Raza, Nivel, ID_Estado, ID_Equipamiento) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_usuario, nombre_personaje, id_raza, 1, id_estado, id_equipamiento))
            connection.commit()
            print("Personaje creado exitosamente.")
    except pymysql.Error as e:
        print(f"Error al crear el personaje: {e}")
    finally:
        connection.close()




def obtener_personajes():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM personaje"
            cursor.execute(sql)
            result = cursor.fetchall()
            return [Personaje(**char) for char in result]
    finally:
        connection.close()

def crear_personaje_equipamiento(id_personaje, id_equipamiento, equipados):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO personaje_equipamiento (id_personaje, id_Equipamiento, equipados) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id_personaje, id_equipamiento, equipados))
        connection.commit()
    finally:
        connection.close()
