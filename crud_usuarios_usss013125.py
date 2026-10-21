from mysql.connector.errors import Error
import conexion

db = conexion.Conexion()


class crud_usuarios_usss013125:
    def consultar(self, buscar):
        # Protegemos los datos sensibles: NO seleccionamos la clave para evitar filtraciones en el navegador
        sql = f"SELECT idUsuario, usuario, nombre, direccion, telefono FROM usuarios_usss013125 WHERE nombre LIKE '%{buscar}%' OR usuario LIKE '%{buscar}%'"
        return db.consultar(sql)

    def login(self, usuario, clave):
        # Valida credenciales contra la base de datos sin filtrar la clave en la respuesta
        sql = "SELECT idUsuario, usuario, nombre, direccion, telefono FROM usuarios_usss013125 WHERE usuario = %s AND clave = %s"
        resultado = db.consultar(sql, (usuario, clave))
        if resultado and len(resultado) > 0:
            return resultado[0]
        return None

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO usuarios_usss013125(usuario,clave,nombre,direccion,telefono)
                    VALUES(%s,%s,%s,%s,%s)
                """
                valores = (
                    datos['usuario'],
                    datos['clave'],
                    datos['nombre'],
                    datos['direccion'],
                    datos['telefono']
                )
            elif datos['accion'] == 'modificar':
                # Si se proporcionó una nueva clave, se actualiza junto con los demás datos
                if datos.get('clave') and str(datos['clave']).strip() != "":
                    sql = """
                        UPDATE usuarios_usss013125 SET usuario=%s,clave=%s,nombre=%s,direccion=%s,telefono=%s
                        WHERE idUsuario=%s
                    """
                    valores = (
                        datos['usuario'],
                        datos['clave'],
                        datos['nombre'],
                        datos['direccion'],
                        datos['telefono'],
                        datos['idUsuario']
                    )
                else:
                    sql = """
                        UPDATE usuarios_usss013125 SET usuario=%s,nombre=%s,direccion=%s,telefono=%s
                        WHERE idUsuario=%s
                    """
                    valores = (
                        datos['usuario'],
                        datos['nombre'],
                        datos['direccion'],
                        datos['telefono'],
                        datos['idUsuario']
                    )
            else:
                sql = """
                    DELETE FROM usuarios_usss013125 WHERE idUsuario=%s
                """
                valores = (datos['idUsuario'],)

            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al guardar el usuario: {e}"


if __name__ == "__main__":
    crud = crud_usuarios_usss013125()
    print("Prueba de consulta:", crud.consultar(""))
