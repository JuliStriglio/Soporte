from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.core.paginator import Paginator
# Create your views here.

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import Producto  # Asegúrate de que el modelo Producto esté importado

def scrapProductosLaReina():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    links = [
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx',
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=03020100&TM=cx',
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=01100700&TM=cx',
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=01020100&TM=cx',
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=01101000&TM=cx',
        # Añade tus enlaces aquí
    ]

    for link in links:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraer productos
                productos = soup.find_all('div', class_='InfoProd')
                for producto in productos:
                    nombre_elemento = producto.find('div', class_='desc')
                    precio_elemento = producto.find('div', class_='izq') or producto.find('div', class_='der')

                    # Verificar y convertir el precio
                    if precio_elemento:
                        precio_text = precio_elemento.text.strip()
                        try:
                            precio = float(precio_text.replace('$', '').replace('.', '').replace(',', '.'))
                        except ValueError:
                            print(f"Error: No se pudo convertir el precio a un número. precio: {precio_text}")
                            continue
                    else:
                        print("Error: No se encontró el precio en la página.")
                        continue

                    # Buscar la imagen
                    foto_elemento = producto.find_previous('div', class_='FotoProd')
                    if foto_elemento:
                        img_tag = foto_elemento.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            foto_url = img_tag['src']
                            if not foto_url.startswith('http'):
                                foto_url = 'https://www.lareinaonline.com.ar/' + foto_url
                        else:
                            foto_url = 'No disponible'
                    else:
                        foto_url = 'No disponible'

                    # Guardar en la base de datos si el nombre y el precio existen
                    if nombre_elemento:
                        nombre = nombre_elemento.text.strip()
                        try:
                            producto = Producto(
                                descripcion=nombre,
                                supermercado='la reina',
                                imagen=foto_url,
                                precio=precio,
                                fecha_act=datetime.today()
                            )
                            producto.save()
                            print(f"Producto '{nombre}' guardado exitosamente.")
                        except Exception as e:
                            print(f"Error al guardar el producto '{nombre}': {e}")
            else:
                print(f"No se pudo acceder a {link}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {link}: {e}")

    return "Scraping y guardado completados."




def mostrar_resultados_lareina(request):
    verificar()
    resultados = Producto.objects.all()
    paginator = Paginator(resultados, 5)  # 5 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Renderizar la plantilla con los resultados paginados
    return render(request, 'productos.html', {'page_obj': page_obj})


def verificar():
    fecha_hoy = datetime.now().date()
    producto = Producto.objects.filter(fecha_act__date=fecha_hoy).last()  # Usamos __date para comparar fechas

    if not producto:  # Si no hay productos de hoy, ejecutamos el scraping
        scrapProductosLaReina()
        Producto.objects.all().update(fecha_act=datetime.now())
    else:
        print('Los datos ya están actualizados para hoy.')