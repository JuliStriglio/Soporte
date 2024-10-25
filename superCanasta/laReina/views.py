from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.core.paginator import Paginator
# Create your views here.

def scrapProductosLaReina():
    # Lista de enlaces que deseas analizar
    links = [
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx',
        'https://www.lareinaonline.com.ar/productosnl.asp?nl=03020100&TM=cx',
        # Añade tus enlaces aquí
    ]
    
    datos = []

    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraer productos
                productos = soup.find_all('div', class_='InfoProd')
                for producto in productos:
                    nombre_elemento = producto.find('div', class_='desc')
                    precio_elemento = producto.find('div', class_='izq')

                    if precio_elemento:
                            precio = precio_elemento.text.strip()
                    else:
                            precio_elemento = producto.find('div', class_='der')
                            precio = precio_elemento.text.strip()    

                    # Buscar la imagen directamente dentro del div del producto
                    foto_elemento = producto.find_previous('div', class_='FotoProd')
                    
                    if foto_elemento:
                        img_tag = foto_elemento.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            foto_url = img_tag['src']
                            # Verificar si la URL de la imagen es completa o relativa
                            if not foto_url.startswith('http'):
                                foto_url = 'https://www.lareinaonline.com.ar/' + foto_url
                        else:
                            foto_url = 'No disponible'
                    else:
                        foto_url = 'No disponible'
                    
                    # Asegúrate de que las variables 'nombre' y 'precio' tengan valores
                    if nombre_elemento and precio_elemento:
                        nombre = nombre_elemento.text.strip()
                        precio = precio_elemento.text.strip()
                        datos.append({
                            'URL': link,
                            'Producto': nombre,
                            'Precio': precio,
                            'Foto': foto_url
                        })
                    else:
                        datos.append({
                            'URL': link, 
                            'Producto': 'Elemento no encontrado', 
                            'Precio': 'N/A', 
                            'Foto': 'No disponible'
                        })
            else:
                datos.append({
                    'URL': link, 
                    'Producto': 'Error', 
                    'Precio': f"No se pudo acceder, status code: {response.status_code}", 
                    'Foto': 'No disponible'
                })
        except requests.exceptions.RequestException as e:
            datos.append({
                'URL': link, 
                'Producto': 'Error', 
                'Precio': str(e), 
                'Foto': 'No disponible'
            })

    # Convertir los datos a un DataFrame de pandas y luego a una lista de diccionarios
    df = pd.DataFrame(datos)
    return df.to_dict(orient='records')



def mostrar_resultados(request):
    resultado = scrapProductosLaReina()

    # Configurar la paginación
    paginator = Paginator(resultado, 5)
    pagina = request.GET.get('page')
    page_obj = paginator.get_page(pagina)

    # Renderizar la plantilla con los resultados paginados
    return render(request, 'productos.html', {'page_obj': page_obj})


    