from django.urls import path 
from canasta.views import inicio, supermercados, ofertas, busqueda

urlpatterns = [
    
    path('',inicio , name='inicio' ),
    path('supermercados/', supermercados, name='supermercados'),
    path('ofertas/', ofertas, name='ofertas'),
    path('busqueda/', busqueda, name='busqueda'),


]