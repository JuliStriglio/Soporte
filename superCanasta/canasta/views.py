from django.shortcuts import redirect, render
from .models import CanastaBasica
from coto.models import Producto
from laReina.models import Producto
from django.core.paginator import Paginator

def inicio(request) : 
    
    return render(request , r'canasta\inicio.html' )

def supermercados(request) : 
    
    return render(request , r'canasta\supermercados.html' )

def busqueda(request) : 

    query = request.GET.get('q', '')
    
    # Filtrar productos en ambas tablas
    productos_coto = Producto.objects.filter(descripcion__icontains=query) if query else Producto.objects.all()
    productos_la_reina = Producto.objects.filter(descripcion__icontains=query) if query else Producto.objects.all()
    
    # Anotar el origen del supermercado
    for producto in productos_coto:
        producto.supermercado = "coto"
    for producto in productos_la_reina:
        producto.supermercado = "la Reina"
    
    # Combina los resultados
    productos = list(productos_coto) + list(productos_la_reina)
    
    # Configuración de la paginación
    paginator = Paginator(productos, 4)  # 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request , r'canasta\busqueda.html',  {'page_obj': page_obj} )

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