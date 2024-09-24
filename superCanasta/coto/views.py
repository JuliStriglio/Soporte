from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.core.paginator import Paginator

# Create your views here.
def scrapProductosCoto() :
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

    links = ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-infusiones/_/N-dw58vw']



# Listas para almacenar datos
    productos = []
    precios = []


    for link in links:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraer información específica
                if 'cotodigital3.com.ar' in link:
                    nombres = soup.find_all('div', class_='descrip_full')
                    precios_info = soup.find_all('div', class_='info_discount')

                    # Asegurarse de que el número de nombres y precios coincidan
                    for nombre, precio_info in zip(nombres, precios_info):
                        nombre_elemento = nombre.text.strip()
                        precio_elemento = precio_info.find('span', class_='atg_store_newPrice')

                        if precio_elemento:
                            precio = precio_elemento.text.strip()
                            productos.append(nombre_elemento)
                            precios.append(precio)
                        else:
                            productos.append(nombre_elemento)
                            precio_elemento = precio_info.find('span', class_='price_discount_gde')
                            precio = precio_elemento.text.strip()
                            precios.append(precio)

                else:
                    print(f"Contenido de {link}:\n{response.text[:200]}...")

            else:
                print(f"No se pudo acceder a {link}_, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {link}: {e}")

    # Crear un DataFrame de pandas con los datos extraídos
    df = pd.DataFrame({'Producto': productos, 'Precio': precios})

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



