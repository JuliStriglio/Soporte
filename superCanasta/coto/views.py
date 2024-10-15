from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.core.paginator import Paginator

# Create your views here.

def scrapProductosCoto():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    links = ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-infusiones/_/N-dw58vw']

    # Listas para almacenar datos
    productos = []
    precios = []
    imagenes = []

    for link in links:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraer información específica
                if 'cotodigital3.com.ar' in link:
                    nombres = soup.find_all('div', class_='descrip_full')
                    precios_info = soup.find_all('div', class_='info_discount')
                    imagenes_info = soup.find_all('div', class_='product_info_container') # Clase del contenedor de imagenes

                    # Asegurarse de que el número de nombres, precios e imágenes coincidan
                    for nombre, precio_info, imagen_info in zip(nombres, precios_info, imagenes_info):
                        nombre_elemento = nombre.text.strip()
                        precio_elemento = precio_info.find('span', class_='atg_store_newPrice')

                        if precio_elemento:
                            precio = precio_elemento.text.strip()
                        else:
                            precio_elemento = precio_info.find('span', class_='price_discount_gde')
                            precio = precio_elemento.text.strip()

                        # Obtener la URL de la imagen
                        img_tag = imagen_info.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            imagen_url = img_tag['src']
                        else:
                            imagen_url = 'No disponible'

                        # Añadir a las listas
                        productos.append(nombre_elemento)
                        precios.append(precio)
                        imagenes.append(imagen_url)

                else:
                    print(f"Contenido de {link}:\n{response.text[:200]}...")

            else:
                print(f"No se pudo acceder a {link}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {link}: {e}")

    # Crear un DataFrame de pandas con los datos extraídos
    df = pd.DataFrame({'Producto': productos, 'Precio': precios, 'Imagen': imagenes})

    # Retornar los resultados como lista de diccionarios para pasarlos a la vista
    resultados = df.to_dict(orient='records')
    return resultados



def mostrar_resultados_coto (request) :
    resultados = scrapProductosCoto()
    
    paginator = Paginator(resultados, 5)  # 10 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con los resultados
    return render(request, 'coto/productos.html', {'page_obj': page_obj})



