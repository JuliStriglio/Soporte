from django.urls import path 
from laReina.views import scrapProductosLaReina

urlpatterns = [
    
    path('', scrapProductosLaReina, name = 'scrapProductosLaReina'),

]