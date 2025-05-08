# 🛡️ Sistema de Login Seguro con Python, MySQL y Docker

Este proyecto implementa un sistema de registro e inicio de sesión de usuarios con protección de datos sensibles (encriptación con `cryptography`, hashes de contraseña con `bcrypt`) y una base de datos MySQL. El sistema está completamente contenido en Docker para facilitar su despliegue.

---

## 📁 Estructura del Proyecto

ProyectoFinal-DevOps/
│
├── login.py # Script principal para registrar e iniciar sesión
├── clave.key # Clave de encriptación generada automáticamente
├── Dockerfile # Construye la imagen de la app
├── docker-compose.yml # Orquesta los servicios app y db
└── README.md # Este archivo

---

## 🚀 Tecnologías Utilizadas

- Python 3.11
- MySQL 8.0
- Docker & Docker Compose
- bcrypt (hashing de contraseñas)
- cryptography (encriptación de datos)
- mysql-connector-python

---

## ⚙️ Configuración Inicial

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/ProyectoFinal-DevOps.git
   cd ProyectoFinal-DevOps

2. Levanta los contenedores:
  docker-compose up -d
Esto iniciará:

Un contenedor MySQL (mysql_login_db)

Una app Python (sistema_login_app)

3. Crea las tablas en la base de datos:
  Conéctate al contenedor de MySQL:
  docker exec -it mysql_login_db mysql -u root -p

Ejecuta en la terminal SQL:
DROP DATABASE IF EXISTS ProyectoFinal_DevOpsDB;
CREATE DATABASE ProyectoFinal_DevOpsDB;
USE ProyectoFinal_DevOpsDB;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE datos_personales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    genero ENUM('Masculino', 'Femenino', 'Otro'),
    direccion_encriptada BLOB,
    curp_encriptado BLOB,
    rfc_encriptado BLOB,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

🧪 Uso
1. Ejecuta la app:
   docker exec -it sistema_login_app python login.py

2. Desde el menú:

  Opción 1: Registrar nuevo usuario
  
  Opción 2: Iniciar sesión
  
  Opción 3: Salir
  
  Los datos sensibles como dirección, CURP y RFC se almacenan en la base de datos encriptados, y las contraseñas están hasheadas.

  🛑 Detener los servicios
    docker-compose down


🧩 Notas
  La clave de encriptación (clave.key) se genera automáticamente al ejecutar el sistema por primera vez.
  
  Asegúrate de mantener esta clave segura; sin ella no podrás desencriptar los datos almacenados.

📄 Licencia
  MIT License. Puedes usar, modificar y distribuir este proyecto libremente.
