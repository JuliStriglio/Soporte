from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.

def scrapProductosLaReina (request) :
    
    links = [
    'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx',
    'https://www.lareinaonline.com.ar/productosnl.asp?nl=03020100&TM=cx',  # Ejemplo adicional
    ]

    resultados = []

    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraer información específica si la URL es de 'lareinaonline'
                if 'lareinaonline.com.ar' in link:
                    productos = soup.find_all('div', class_='InfoProd')
                    for producto in productos:
                        nombre_elemento = producto.find('div', class_='desc')
                        precio_elemento = producto.find('div', class_='izq')
                        if nombre_elemento and precio_elemento:
                            nombre = nombre_elemento.text.strip()
                            precio = precio_elemento.text.strip()
                            resultados.append(f'Producto: {nombre}, Precio: {precio}')
                        else:
                            resultados.append(f'Elemento no encontrado en {link}, revisa los selectores.')
                else:
                    # Para otros links, mostrar los primeros 200 caracteres del contenido
                    resultados.append(f"Contenido de {link}:\n{response.text[:200]}...")

            else:
                resultados.append(f"No se pudo acceder a {link}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            resultados.append(f"Error al acceder a {link}: {e}")

    # Convertir la lista de resultados en una única cadena de texto
    resultados_str = "\n\n".join(resultados)

    # Mostrar los resultados en la consola
    print(resultados_str)

    # Opcional: Guardar los resultados en un archivo de texto
    with open('resultados_scraping.txt', 'w') as archivo:
        archivo.write(resultados_str)

        
        return render(request)