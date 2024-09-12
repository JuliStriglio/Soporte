from django.urls import path 
from coto.views import mostrar_resultados_coto

urlpatterns = [
    
    path('resultados/', mostrar_resultados_coto, name = 'mostrar_resultados_coto'),

]