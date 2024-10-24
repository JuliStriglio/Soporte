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

    
#    links = [
#    'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx',
#    'https://www.lareinaonline.com.ar/productosnl.asp?nl=03020100&TM=cx',  # Ejemplo adicional
#    ]

#    resultados = []

#    for link in links:
#        try:
 #           response = requests.get(link)
 #           if response.status_code == 200:
 #               soup = BeautifulSoup(response.text, 'html.parser')
#
 #               # Extraer información específica si la URL es de 'lareinaonline'
 #               if 'lareinaonline.com.ar' in link:
 #                   productos = soup.find_all('div', class_='InfoProd')
#                   for producto in productos:
#                        nombre_elemento = producto.find('div', class_='desc')
#                        precio_elemento = producto.find('div', class_='izq')
 #                       if nombre_elemento and precio_elemento:
 #                          nombre = nombre_elemento.text.strip()
   #                         precio = precio_elemento.text.strip()
  #                          resultados.append(f'Producto: {nombre}, Precio: {precio}')
 #                       else:
 #                           resultados.append(f'Elemento no encontrado en {link}, revisa los selectores.')
  #              else:
  #                  # Para otros links, mostrar los primeros 200 caracteres del contenido
  #                  resultados.append(f"Contenido de {link}:\n{response.text[:200]}...")
#
  #          else:
  #              resultados.append(f"No se pudo acceder a {link}, status code: {response.status_code}")
   #     except requests.exceptions.RequestException as e:
   #         resultados.append(f"Error al acceder a {link}: {e}")

  #  # Convertir la lista de resultados en una única cadena de texto
  #  resultados_str = "\n\n".join(resultados)

  #  # Mostrar los resultados en la consola
   # print(resultados_str)

  #  # Opcional: Guardar los resultados en un archivo de texto
  #  with open('resultados_scraping.txt', 'w') as archivo:
   #     archivo.write(resultados_str)

        
    #return render(request, r'laReina/productos.html' )


    