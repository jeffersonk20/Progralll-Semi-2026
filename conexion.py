import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(self, database="db_academica"):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = ""
        self.database = database
        self.puerto_conectado = None
        self.conexion = None
        self.conectar()

    def conectar(self):
        """
        Intenta conectarse a MySQL en los puertos habituales (3306 y 3307)
        utilizando el conector nativo puro de Python.
        """
        puertos = [3306, 3307]
        for puerto in puertos:
            try:
                params = {
                    "host": self.host,
                    "port": puerto,
                    "user": self.user,
                    "password": self.password,
                    "use_pure": True,
                    "charset": "utf8mb4"
                }
                if self.database:
                    params["database"] = self.database

                cnx = mysql.connector.connect(**params)
                if cnx.is_connected():
                    self.conexion = cnx
                    self.puerto_conectado = puerto
                    print(f"Conectado a MySQL en el puerto {puerto}")
                    return True
            except Error:
                continue

        # Intento sin base de datos por si aún no existe
        if self.database:
            for puerto in puertos:
                try:
                    cnx = mysql.connector.connect(
                        host=self.host,
                        port=puerto,
                        user=self.user,
                        password=self.password,
                        use_pure=True,
                        charset="utf8mb4"
                    )
                    if cnx.is_connected():
                        self.conexion = cnx
                        self.puerto_conectado = puerto
                        print(f"Conectado al servidor MySQL en el puerto {puerto} (sin BD seleccionada)")
                        return True
                except Error:
                    continue

        print("Error: No se pudo conectar a la base de datos en los puertos 3306 ni 3307.")
        return False

    def consultar(self, sql, datos=None):
        try:
            if not self.conexion or not self.conexion.is_connected():
                self.conectar()
            cursor = self.conexion.cursor(dictionary=True)
            if datos:
                cursor.execute(sql, datos)
            else:
                cursor.execute(sql)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return []

    def ejecutar(self, sql, datos=None):
        try:
            if not self.conexion or not self.conexion.is_connected():
                self.conectar()
            cursor = self.conexion.cursor()
            if datos:
                cursor.execute(sql, datos)
            else:
                cursor.execute(sql)
            self.conexion.commit()
            cursor.close()
            return 'ok'
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return f"Error: {e}"


if __name__ == "__main__":
    db = Conexion()
