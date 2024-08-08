from django.shortcuts import render

def inicio (request) :
    return render(request , r'pagina\inicio.html' )