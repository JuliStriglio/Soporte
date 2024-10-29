from django.urls import path 
from laReina.views import mostrar_resultados_lareina

urlpatterns = [
    
    path('resultados/', mostrar_resultados_lareina, name = 'mostrar_resultados_lareina'),

]