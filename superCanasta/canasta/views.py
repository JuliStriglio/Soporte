from django.shortcuts import render

def inicio(request) : 
    
    return render(request , r'canasta\inicio.html' )

def supermercados(request) : 
    
    return render(request , r'canasta\supermercados.html' )

def ofertas(request) : 
    
    return render(request , r'canasta\ofertas.html' )

def busqueda(request) : 
    
    return render(request , r'canasta\busqueda.html' )