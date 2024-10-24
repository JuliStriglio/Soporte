from django.shortcuts import redirect, render
from .models import CanastaBasica

def inicio(request) : 
    
    return render(request , r'canasta\inicio.html' )

def supermercados(request) : 
    
    return render(request , r'canasta\supermercados.html' )

def busqueda(request) : 
    
    return render(request , r'canasta\busqueda.html' )

def canasta(request):
    productos_canasta = CanastaBasica.objects.all()
    return render(request, 'canasta/canasta.html', {'productos_canasta': productos_canasta })

def add_producto(request):
    if request.method == "POST":
        descripcion = request.POST['nombre']
        cantidad = int(request.POST['cantidad'])
        CanastaBasica.objects.create(descripcion=descripcion, cantidad=cantidad)
        return redirect('canasta')
    return redirect('canasta')