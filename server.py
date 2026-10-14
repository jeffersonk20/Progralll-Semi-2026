from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse 
from urllib.parse import urlparse, parse_qs
import crud_clientes
import crud_productos
import crud_periodos

import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudProductos = crud_productos.crud_productos()
crudPeriodos = crud_periodos.crud_periodos()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)

        urlParse = urlparse(self.path)
        modulo = datos.get("modulo", "")

        if modulo == "cliente" or urlParse.path in ["/cliente", "/clientes"]:
            respuesta = {'msg': crudClientes.administrar(datos)}
        elif modulo == "producto" or urlParse.path in ["/producto", "/productos"]:
            respuesta = {'msg': crudProductos.administrar(datos)}
        elif modulo == "periodo" or urlParse.path in ["/periodo", "/periodos"]:
            respuesta = {'msg': crudPeriodos.administrar(datos)}
        else:
            respuesta = {'msg': 'Módulo no reconocido'}

        self.send_response(200)
        self.send_header("Content-type","application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
       
        if urlParse.path == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            datos = crudClientes.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        elif urlParse.path == "/productos":
            buscar = qs.get('buscar', [''])[0]
            datos = crudProductos.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        elif urlParse.path == "/periodos":
            idCliente = qs.get('idCliente', [''])[0]
            datos = crudPeriodos.consultar(idCliente)
            self.send_response(200)
            self.send_header("Content-type","application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))
        
        elif self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif urlParse.path == "/vistas":
            self.path = f"/modulos/{qs.get('form', [''])[0]}.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost",port),miServidor)
server.serve_forever()