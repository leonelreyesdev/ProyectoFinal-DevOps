import mysql.connector
import bcrypt
from cryptography.fernet import Fernet
import os

# === Cargar o generar clave de encriptación ===
CLAVE_PATH = "clave.key"

if not os.path.exists(CLAVE_PATH):
    clave_encriptacion = Fernet.generate_key()
    with open(CLAVE_PATH, "wb") as archivo_clave:
        archivo_clave.write(clave_encriptacion)
    print("✅ Archivo clave.key generado.")
else:
    with open(CLAVE_PATH, "rb") as archivo_clave:
        clave_encriptacion = archivo_clave.read()

fernet = Fernet(clave_encriptacion)

# === Conexión a la base de datos ===
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hiale12345678",
        database="ProyectoFinal_DevOpsDB"
    )

# === Crear nuevo usuario ===
def crear_usuario():
    print("\n--- Registro de nuevo usuario ---")
    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")

    nombre = input("Nombre completo: ")
    correo = input("Correo electrónico: ")
    telefono = input("Teléfono: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    genero = input("Género (Masculino/Femenino/Otro): ")

    direccion = input("Dirección: ")
    curp = input("CURP: ")
    rfc = input("RFC: ")

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    direccion_encriptada = fernet.encrypt(direccion.encode())
    curp_encriptado = fernet.encrypt(curp.encode())
    rfc_encriptado = fernet.encrypt(rfc.encode())

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)",
                       (username, password_hash.decode()))
        id_usuario = cursor.lastrowid

        cursor.execute("""
            INSERT INTO datos_personales 
            (id_usuario, nombre, correo, telefono, fecha_nacimiento, genero, direccion_encriptada, curp_encriptado, rfc_encriptado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, nombre, correo, telefono, fecha_nacimiento, genero,
              direccion_encriptada, curp_encriptado, rfc_encriptado))

        conn.commit()
        print("✅ Usuario registrado correctamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error al registrar: {err}")
    finally:
        cursor.close()
        conn.close()

# === Iniciar sesión ===
def login():
    print("\n--- Inicio de sesión ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password_hash FROM usuarios WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario, password_hash = resultado
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            print("🔓 Acceso concedido.")
            mostrar_datos(id_usuario)
        else:
            print("❌ Contraseña incorrecta.")
    else:
        print("❌ Usuario no encontrado.")

    cursor.close()
    conn.close()

# === Mostrar datos personales del usuario ===
def mostrar_datos(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre, correo, telefono, fecha_nacimiento, genero,
               direccion_encriptada, curp_encriptado, rfc_encriptado
        FROM datos_personales
        WHERE id_usuario = %s
    """, (id_usuario,))
    datos = cursor.fetchone()

    if datos:
        nombre, correo, telefono, fecha_nacimiento, genero, direccion_enc, curp_enc, rfc_enc = datos

        direccion = fernet.decrypt(direccion_enc).decode()
        curp = fernet.decrypt(curp_enc).decode()
        rfc = fernet.decrypt(rfc_enc).decode()

        print("\n🧾 Datos del usuario:")
        print(f"Nombre: {nombre}")
        print(f"Correo: {correo}")
        print(f"Teléfono: {telefono}")
        print(f"Fecha de nacimiento: {fecha_nacimiento}")
        print(f"Género: {genero}")
        print(f"Dirección: {direccion}")
        print(f"CURP: {curp}")
        print(f"RFC: {rfc}")
    else:
        print("⚠️ Datos no encontrados.")

    cursor.close()
    conn.close()

# === Menú principal ===
def main():
    while True:
        print("\n=== Menú ===")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            login()
        elif opcion == "3":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción inválida.")

if __name__ == "__main__":
    main()