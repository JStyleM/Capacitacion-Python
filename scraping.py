import requests
from bs4 import BeautifulSoup

# URL de la página que queremos "scrapear"
url = "https://github.com"

# Hacemos una solicitud GET a la página
response = requests.get(url)

# Verificamos que la solicitud fue exitosa
if response.status_code == 200:

    # Obtenemos el contenido HTML de la página
    html = response.text

    # Parseamos el HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Buscamos todas las etiquetas <h1> y <h2>
    titulos = soup.find_all(["h1", "h2"])

    # Muestra los Resultados Enumerados
    print("Títulos encontrados:")
    for i, titulo in enumerate(titulos, start=1):
        print(f"{i}. {titulo.text.strip()}")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
