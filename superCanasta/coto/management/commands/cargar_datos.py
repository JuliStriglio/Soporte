import os
import csv
from django.core.management.base import BaseCommand
from coto.models import Producto  # Asegúrate de importar tu modelo

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str)

    def handle(self,*args,**kwargs):
        archivo = kwargs['archivo']
        
        if not os.path.exists(archivo):
            self.stdout.write(self.style.ERROR(f'El archivo {archivo} no existe.'))
            return

        with open(archivo, newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)  # Usa DictReader para acceder a los datos del archivo resultados_scraping.csv 
            for fila in lector:
                descripcion = fila['Producto'].strip()
                precio_str = fila['Precio'].replace('$', '').replace('.', '').replace(',', '.')  # lo hace formato decimal
                supermercado = 'coto'
                if precio_str.lower() == 'precio no encontrado':
                    self.stdout.write(self.style.WARNING(f'Producto {descripcion} tiene un precio no encontrado. Ignorando.'))
                    continue

                try:
                    precio = float(precio_str)  # lo convierte en flotante
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Error al convertir el precio para el producto {descripcion}. Ignorando.'))
                    continue

                producto = Producto(descripcion=descripcion, precio=precio, supermercado = supermercado)
                producto.save()
                self.stdout.write(self.style.SUCCESS(f'Producto {descripcion} cargado exitosamente.'))

        self.stdout.write(self.style.SUCCESS('Carga completa exitosamente'))
