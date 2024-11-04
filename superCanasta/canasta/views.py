from django.shortcuts import redirect, render
from canasta.models import CanastaBasica
from coto.models import Producto as ProductoCoto
from laReina.models import Producto as ProductoLaReina
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def inicio(request): 
    return render(request, 'canasta/inicio.html')

def supermercados(request): 
    total_coto = 0
    total_la_reina = 0

    for item in CanastaBasica.objects.all():
        print(item.descripcion)
        producto_coto = ProductoCoto.objects.filter(supermercado='coto', descripcion__icontains=item.descripcion).order_by('precio').first()
        if producto_coto:
            total_coto += producto_coto.precio * item.cantidad

    for item in CanastaBasica.objects.all():
        print(item.descripcion)
        producto_la_reina = ProductoLaReina.objects.filter(supermercado='la reina', descripcion__icontains=item.descripcion).order_by('precio').first()
        if producto_la_reina:
            total_la_reina += producto_la_reina.precio * item.cantidad
        
    return render(request, 'canasta/supermercados.html', {
        'total_la_reina': total_la_reina,
        'total_coto': total_coto
    })

def busqueda(request): 
    query = request.GET.get('q', '')
    
    # Filtrar productos en ambas tablas
    productos_coto = ProductoCoto.objects.filter(descripcion__icontains=query) if query else ProductoCoto.objects.all()
    productos_la_reina = ProductoLaReina.objects.filter(descripcion__icontains=query) if query else ProductoLaReina.objects.all()
    
    # Anotar el origen del supermercado
    for producto in productos_coto:
        producto.supermercado = "coto"
    for producto in productos_la_reina:
        producto.supermercado = "la Reina"
    
    # Combina los resultados
    productos = list(productos_coto) + list(productos_la_reina)
    
    # Configuración de la paginación
    paginator = Paginator(productos, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'canasta/busqueda.html', {'page_obj': page_obj})

def canasta(request):
    productos_canasta = CanastaBasica.objects.all()
    return render(request, 'canasta/canasta.html', {'productos_canasta': productos_canasta })

def add_producto(request):
    if request.method == "POST":
        descripcion = request.POST['nombre']
        cantidad = int(request.POST['cantidad'])
        if cantidad > 0:  # Verifica que la cantidad sea positiva
            CanastaBasica.objects.create(descripcion=descripcion, cantidad=cantidad)
        return redirect('canasta')
    return redirect('canasta')


def delete_producto(request, id):
    if request.method == "POST":
        producto = get_object_or_404(CanastaBasica, id=id)
        producto.delete()
        return redirect('canasta')  