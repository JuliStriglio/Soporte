from django.urls import path 
from canasta.views import inicio, supermercados, canasta, busqueda, add_producto

urlpatterns = [
    
    path('',inicio , name='inicio' ),
    path('supermercados/', supermercados, name='supermercados'),
    path('canasta/', canasta, name='canasta'),
    path('busqueda/', busqueda, name='busqueda'),
    path('add_producto/', add_producto, name='add_producto'),


]