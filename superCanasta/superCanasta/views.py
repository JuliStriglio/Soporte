from django.shortcuts import render

def inicio (request) :
    return render(request , r'pagina\inicio.html' )


def supermercados(request) :
    return render(request, r'pagina\supermercados.html')

def ofertas(request) :
    return render(request, r'pagina\ofertas.html')

def busqueda(request) :
    return render(request, r'pagina\busqueda.html')