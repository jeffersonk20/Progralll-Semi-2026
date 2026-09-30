from mysql.connector.errors import Error
import conexion

db = conexion.Conexion()

class crud_periodos:
    def consultar(self, idCliente):
        try:
            if not idCliente:
                return []
            sql = f"""
                SELECT idPeriodo, idCliente, 
                       DATE_FORMAT(desde, '%Y-%m-%d') AS desde, 
                       DATE_FORMAT(hasta, '%Y-%m-%d') AS hasta, 
                       CAST(balance AS CHAR) AS balance, 
                       codigo, 
                       CAST(precio AS CHAR) AS precio, 
                       estado
                FROM periodos_actividades_economicas 
                WHERE idCliente = {int(idCliente)}
                ORDER BY desde ASC
            """
            resultado = db.consultar(sql)
            return resultado if resultado is not None else []
        except Error as e:
            print(f"Error al consultar periodos: {e}")
            return []

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO periodos_actividades_economicas(idCliente, desde, hasta, balance, codigo, precio, estado)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    datos['idCliente'],
                    datos['desde'],
                    datos['hasta'],
                    datos['balance'],
                    datos.get('codigo', '11801'),
                    datos['precio'],
                    datos.get('estado', 'Histórico')
                )
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE periodos_actividades_economicas 
                    SET desde=%s, hasta=%s, balance=%s, codigo=%s, precio=%s, estado=%s
                    WHERE idPeriodo=%s AND idCliente=%s
                """
                valores = (
                    datos['desde'],
                    datos['hasta'],
                    datos['balance'],
                    datos.get('codigo', '11801'),
                    datos['precio'],
                    datos.get('estado', 'Histórico'),
                    datos['idPeriodo'],
                    datos['idCliente']
                )
            else:
                sql = """
                    DELETE FROM periodos_actividades_economicas WHERE idPeriodo=%s
                """
                valores = (datos['idPeriodo'],)
            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al guardar período: {e}"
