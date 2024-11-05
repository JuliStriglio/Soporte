from datetime import datetime
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Producto
from django.core.paginator import Paginator

# Create your views here.

def scrapProductosCoto():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    links = ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-infusiones/_/N-dw58vw',
             'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-harinas/_/N-842qrm',
             'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-aceites-y-condimentos-aceites/_/N-16r0nc0',
             'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-infusiones-mate/_/N-vra9dh']

    for link in links:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                if 'cotodigital3.com.ar' in link:
                    descripciones = soup.find_all('div', class_='descrip_full')
                    precios_info = soup.find_all('div', class_='info_discount')
                    imagenes_info = soup.find_all('div', class_='product_info_container')

                    for descripcion, precio_info, imagen_info in zip(descripciones, precios_info, imagenes_info):
                        descripcion_elemento = descripcion.text.strip()

                        precio_elemento = precio_info.find('span', class_='atg_store_newPrice')

                        if precio_elemento:
                            precio = precio_elemento.text.strip()
                        else:
                            precio_elemento = precio_info.find('span', class_='price_discount_gde')
                            precio = precio_elemento.text.strip()

                        if precio_elemento:
                            precio_text = precio_elemento.text.strip()
                            try:
                                precio = float(precio_text.replace('$', '').replace('.', '').replace(',', '.'))
                            except ValueError:
                                print('Error: No se pudo convertir el precio a un número. precio:',{precio_text})
                                continue
                        else:
                            print('Error: No se encontró el precio en la página ')
                            continue

                        img_tag = imagen_info.find('img')
                        imagen_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'No disponible'

                        # Guarda el producto en la base de datos
                        if descripcion_elemento:
                         nombre = descripcion_elemento
                        try:
                            producto = Producto(
                                descripcion=nombre,
                                supermercado='coto',
                                imagen=imagen_url,
                                precio=precio,
                                fecha_act=datetime.today()
                            )
                            producto.save()
                            print(f"Producto '{descripcion_elemento}' guardado exitosamente.")
                        except Exception as e:
                            print(f"Error al guardar el producto '{descripcion_elemento}': {e}")
            else:
                print(f"No se pudo acceder a {link}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {link}: {e}")

    return "Scraping y guardado completados."


def mostrar_resultados_coto (request) :
    verificar()
    resultados = Producto.objects.all()
    paginator = Paginator(resultados, 5)  # 5 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Renderizar la plantilla con los resultados
    return render(request, 'coto/productos.html', {'page_obj': page_obj})


def verificar():

    fecha_hoy = datetime.now().date()
    producto = Producto.objects.filter(fecha_act__date=fecha_hoy).last()  # Usamos __date para comparar fechas

    if not producto:  # Si no hay productos de hoy, ejecutamos el scraping
        scrapProductosCoto()
        Producto.objects.all().update(fecha_act=datetime.now())
    else:
        print('Los datos ya están actualizados para hoy.')
