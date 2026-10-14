from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def hola_mundo(request):
    return HttpResponse("Hola mundo")

def saludoNombre(request, nombre):
    return HttpResponse(f"Hola {nombre}, bienvenido a progra")

def edadNombre  (request, nombre, edad):
    return HttpResponse(f"Hola {nombre}, tienes {edad} años", "Bienvenido a progra lll")

def index(request):
    return render(request, 'index.html')

    