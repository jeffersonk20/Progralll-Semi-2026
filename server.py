from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import json
import crud_usuarios_usss013125

port = 3000
crudUsuarios = crud_usuarios_usss013125.crud_usuarios_usss013125()


class miServidor(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Cabeceras de seguridad para prevenir filtraciones y caché de datos confidenciales
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()

    def do_POST(self):
        try:
            longitud = int(self.headers.get('Content-Length', 0))
            cuerpo = self.rfile.read(longitud).decode("utf-8")
            try:
                datos = json.loads(cuerpo)
            except Exception:
                datos = json.loads(parse.unquote(cuerpo))
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'msg': f'Datos inválidos: {e}'}).encode("utf-8"))
            return

        urlParse = urlparse(self.path)
        modulo = datos.get("modulo", "")

        # Autenticación de Login
        if urlParse.path == "/login" or modulo == "login":
            usuario = str(datos.get("usuario", "")).strip()
            clave = str(datos.get("clave", "")).strip()

            usuario_valido = crudUsuarios.login(usuario, clave)
            if usuario_valido:
                # Retornamos los datos seguros sin la clave para no exponer credenciales
                respuesta = {
                    'status': 'ok',
                    'msg': 'Acceso concedido',
                    'usuario': {
                        'idUsuario': usuario_valido['idUsuario'],
                        'usuario': usuario_valido['usuario'],
                        'nombre': usuario_valido['nombre']
                    }
                }
            else:
                respuesta = {
                    'status': 'error',
                    'msg': 'Acceso denegado: Usuario o contraseña no registrados.'
                }

        # Gestión CRUD de Usuarios
        elif modulo == "usuarios" or urlParse.path in ["/usuarios", "/usuario"]:
            resultado = crudUsuarios.administrar(datos)
            respuesta = {'status': 'ok' if resultado == 'ok' else 'error', 'msg': resultado}
        else:
            respuesta = {'status': 'error', 'msg': 'Módulo no reconocido'}

        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # Búsqueda / Consulta de Usuarios
        if urlParse.path in ["/usuarios", "/usuario"]:
            buscar = qs.get('buscar', [''])[0]
            # Devuelve usuarios SIN la contraseña para evitar filtración en el navegador
            datos = crudUsuarios.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        elif self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif urlParse.path == "/vistas":
            form = qs.get('form', [''])[0]
            self.path = f"/modulos/{form}.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        else:
            return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    print("=" * 60)
    print(f"  Servidor iniciado en http://localhost:{port}")
    print("  Presiona CTRL+C para detener el servidor.")
    print("=" * 60)
    servidor = HTTPServer(("localhost", port), miServidor)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
