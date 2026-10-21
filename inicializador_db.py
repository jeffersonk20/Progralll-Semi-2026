import os
import mysql.connector
from mysql.connector import Error


def inicializar():
    print("=" * 60)
    print("  INICIALIZADOR DE BASE DE DATOS Y TABLA - PARCIAL II")
    print("  Estudiante: usss013125 | Base de Datos: db_academica")
    print("=" * 60)

    host = "127.0.0.1"
    user = "root"
    password = ""
    puertos = [3306, 3307]

    cnx = None
    puerto_activo = None

    # Intentar conexión al servidor MySQL
    for p in puertos:
        try:
            temp_cnx = mysql.connector.connect(
                host=host,
                port=p,
                user=user,
                password=password,
                use_pure=True,
                charset="utf8mb4"
            )
            if temp_cnx.is_connected():
                cnx = temp_cnx
                puerto_activo = p
                print(f"[+] Conectado a MySQL exitosamente en el puerto {p}")
                break
        except Error:
            continue

    if not cnx:
        print("[-] Error: No se pudo conectar a MySQL en los puertos 3306 ni 3307.")
        print("    Asegúrate de que MySQL (XAMPP / MariaDB) esté iniciado.")
        return False

    cursor = cnx.cursor()

    try:
        # 1. Crear Base de Datos
        print("[+] Verificando/creando base de datos 'db_academica'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_academica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute("USE db_academica;")

        # 2. Crear Tabla usuarios_usss013125
        print("[+] Verificando/creando tabla 'usuarios_usss013125'...")
        crear_tabla_sql = """
        CREATE TABLE IF NOT EXISTS usuarios_usss013125 (
            idUsuario INT(10) NOT NULL AUTO_INCREMENT,
            usuario CHAR(35) NOT NULL UNIQUE,
            clave CHAR(35) NOT NULL,
            nombre CHAR(85) NOT NULL,
            direccion CHAR(100) NOT NULL,
            telefono CHAR(9) NOT NULL,
            PRIMARY KEY (idUsuario)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(crear_tabla_sql)

        # 3. Insertar usuario inicial si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM usuarios_usss013125;")
        total_usuarios = cursor.fetchone()[0]
        if total_usuarios == 0:
            print("[+] Insertando usuario de prueba inicial (usss013125)...")
            insert_sql = """
            INSERT INTO usuarios_usss013125 (usuario, clave, nombre, direccion, telefono)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_sql, (
                "usss013125",
                "12345",
                "Jefferson Castillo",
                "Usulután, El Salvador",
                "7000-0000"
            ))
            cnx.commit()
            print("[+] Usuario inicial creado:")
            print("    - Usuario: usss013125")
            print("    - Clave:   12345")
        else:
            print(f"[i] La tabla ya cuenta con {total_usuarios} usuario(s) registrado(s).")

        # 4. Generar el script SQL para exportación junto a este archivo
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_sql = os.path.join(ruta_script, "db_academica.sql")
        
        contenido_sql = """-- ==========================================================
-- ARCHIVO DE EXPORTACIÓN DE BASE DE DATOS
-- PARCIAL II - PROGRAMACIÓN III
-- Estudiante: usss013125
-- Base de Datos: db_academica
-- Tabla: usuarios_usss013125
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `db_academica` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `db_academica`;

-- --------------------------------------------------------
-- Estructura de tabla para la tabla `usuarios_usss013125`
-- --------------------------------------------------------

DROP TABLE IF EXISTS `usuarios_usss013125`;
CREATE TABLE `usuarios_usss013125` (
  `idUsuario` int(10) NOT NULL AUTO_INCREMENT,
  `usuario` char(35) NOT NULL,
  `clave` char(35) NOT NULL,
  `nombre` char(85) NOT NULL,
  `direccion` char(100) NOT NULL,
  `telefono` char(9) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `idx_usuario` (`usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Volcado de datos para la tabla `usuarios_usss013125`
-- --------------------------------------------------------

INSERT INTO `usuarios_usss013125` (`idUsuario`, `usuario`, `clave`, `nombre`, `direccion`, `telefono`) VALUES
(1, 'usss013125', '12345', 'Jefferson Castillo', 'Usulután, El Salvador', '7000-0000'),
(2, 'docente', 'docente123', 'Profesor Evaluador', 'San Salvador', '7123-4567');
"""
        with open(ruta_sql, "w", encoding="utf-8") as f:
            f.write(contenido_sql)

        print(f"[+] Archivo SQL exportado exitosamente en:\n    {ruta_sql}")
        print("=" * 60)
        print("  ¡INICIALIZACIÓN COMPLETADA CON ÉXITO!")
        print("=" * 60)
        return True

    except Error as e:
        print(f"[-] Error durante la inicialización: {e}")
        return False
    finally:
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    inicializar()
