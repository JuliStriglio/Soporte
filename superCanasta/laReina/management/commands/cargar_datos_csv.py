import os
import csv
from django.core.management.base import BaseCommand
from canasta.models import Producto  # Asegúrate de importar tu modelo

class Command(BaseCommand):
    help = 'resultado_scraping.csv'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='resultados_scraping.csv')

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        
        if not os.path.exists(archivo):
            self.stdout.write(self.style.ERROR(f'El archivo {archivo} no existe.'))
            return

        with open(archivo, newline='', encoding='utf-8') as f:
            lector = csv.reader(f)
            for fila in lector:
                if len(fila) != 2:  # Asegúrate de que hay exactamente 2 columnas
                    self.stdout.write(self.style.WARNING('Fila ignorada: debe contener nombre y cantidad.'))
                    continue
                
                nombre, cantidad = fila
                producto = Producto(descripcion=nombre, cantidad=int(cantidad))  # Ajusta según tu modelo
                producto.save()
                self.stdout.write(self.style.SUCCESS(f'Producto {nombre} cargado exitosamente.'))

        self.stdout.write(self.style.SUCCESS('Carga completada desde CSV.'))
