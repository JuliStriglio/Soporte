from django.urls import path 
from laReina.views import scrapProductosLaReina, mostrar_resultados

urlpatterns = [
    
    path('resultados/', mostrar_resultados, name = 'mostrar_resultados'),

]