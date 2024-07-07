from app.crud import crear_personaje, usuario_existe

def insertar_personaje(id_usuario, nombre_personaje, id_raza, id_estado, id_equipamiento=1):
    if usuario_existe(id_usuario):
        crear_personaje(id_usuario, nombre_personaje, id_raza, id_estado, id_equipamiento)
    else:
        print(f"Error: El usuario con ID {id_usuario} no existe.")

# Ejemplo de uso
if __name__ == "__main__":
    insertar_personaje(1, "Gandalf", 1, 1, 2)  # Suponiendo que el ID de usuario 1 existe
