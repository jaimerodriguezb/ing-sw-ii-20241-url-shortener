import requests
from datetime import datetime, timezone
import binascii

# Algoritmo para realizar el hashing
def base62_encode(value):
    value = int(value)
    base62chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    base = len(base62chars)
    encoded = ''

    while value > 0:
        remainder = value % base
        encoded = base62chars[remainder] + encoded
        value = int(value / base)

    return encoded

# Tokens para conectarse a Notion en la B.D
TOKEN_FOR_NOTION = "secret_PEF343ZLjwQiHRqomIL67F1gaCuo4iksw7sYoK3ZxFn"
TABLE_URL_FOR_USERS = "fa4cf4991442476798e83063c5983fc0"
TABLE_USER = "7ab0e7992dff4e77a8501642636730d5"
TABLE_DETECTED_PSH_URL = "1b70a4030dc34db891b8a6845a9e0fa3"

headers = {
    "Authorization": "Bearer " + TOKEN_FOR_NOTION,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Función para consultar URL
def Consult_data_from_TABLE_URL_FOR_USERS():
    url = f"https://api.notion.com/v1/databases/{TABLE_URL_FOR_USERS}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    # No es necesario guardar los resultados en un archivo JSON
    # with open('db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results 

# Función para consultar en la tabla de phishing en URL
def Consult_data_from_TABLE_DETECTED_PSH_URL():
    url = f"https://api.notion.com/v1/databases/{TABLE_DETECTED_PSH_URL}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    results = data["results"]
    return results

# Encontrar el último ID para tabla de URLs
def get_latest_url_id(urls):
    # Encontrar el último URL_ID utilizado
    latest_url_id = 0
    for url in urls:
        if "URL_ID" in url["properties"]:
            url_id = int(url["properties"]["URL_ID"]["title"][0]["text"]["content"])
            latest_url_id = max(latest_url_id, url_id)

    return latest_url_id

def Acortar_URL(url_acortar):
    return base62_encode(binascii.crc32(url_acortar.encode()))

def Create_new_URL(URL, table):

    # Generar una URL acortada
    # Aquí puedes usar un servicio de acortamiento de URL o crear tu propio esquema de acortamiento, en este caso se usa una funcion para
    # Acortar la URL seguido del localhost 3000 que es donde estara la UI
    short_url = f"{Acortar_URL(URL)}"  # Reemplaza esto con tu lógica de acortamiento de URL

    # Verifica que tabla es la que debe manejar
    urls = Consult_data_from_TABLE_URL_FOR_USERS() if table == TABLE_URL_FOR_USERS else Consult_data_from_TABLE_DETECTED_PSH_URL()

    # Verificar si la URL ya existe en la base de datos
    if Check_existing_URL(URL, urls):
        return short_url if table == TABLE_URL_FOR_USERS else ""

    # Generar el próximo URL_ID
    next_url_id = get_latest_url_id(urls) + 1

    # Crear un nuevo registro de URL en la tabla TABLE_URL_FOR_USERS
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": table},
        "properties": {
            "URL_ID": {"title": [{"text": {"content": str(next_url_id)}}]},
            "URL": {"url": URL},
            "Short_URL": {"url": short_url},
            "Fecha": {"date": {"start": datetime.now().astimezone(timezone.utc).isoformat()}}
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return short_url
    else:
        return f"Error al crear la URL: {response.text}"

def Check_existing_URL(URL, urls):
    # Verificar si la URL ya existe en la base de datos
    for url_entry in urls:
        if "URL" in url_entry["properties"]:
            url_in_db = url_entry["properties"]["URL"]["url"]
            if url_in_db == URL:
                return True

    return False

def Create_new_URL_PSH(URL, table):
    # Consultar los datos de la tabla TABLE_DETECTED_PSH_URL
    urls = Consult_data_from_TABLE_DETECTED_PSH_URL()

    # Verificar si la URL ya existe en la base de datos
    if Check_existing_URL(URL, urls):
        return "Es_Pishing"

    # Generar el próximo URL_ID
    next_url_id = get_latest_url_id(urls) + 1

    # Crear un nuevo registro de URL en la tabla Detected psh URL
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": table},
        "properties": {
            "URL_ID": {"title": [{"text": {"content": str(next_url_id)}}]},
            "URL": {"url": URL},
            "Fecha": {"date": {"start": datetime.now().astimezone(timezone.utc).isoformat()}}
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return 0
    else:
        return f"Error al crear la URL: {response.text}"

#URL = "https://www.alkosto.com/celulares/smartphones/c/BI_101_ALKOS?sort=price-asc&range=0-&q=%3Aprice-asc%3Ared-transmision-datos%3A5G"
#print(Create_new_URL(URL, TABLE_URL_FOR_USERS))

#URL = "https://www.ejemplopsh.com"
#print(Create_new_URL_PSH(URL, TABLE_DETECTED_PSH_URL))

def get_original_url_from_short_url(short_url):
    # Consultar los datos de la tabla URL_FOR_USERS
    urls = Consult_data_from_TABLE_URL_FOR_USERS()

    # Buscar la URL original basada en la Short_URL proporcionada
    for url_entry in urls:
        if "Short_URL" in url_entry["properties"]:
            short_url_in_db = url_entry["properties"]["Short_URL"]["url"]
            if short_url_in_db == short_url:
                original_url = url_entry["properties"]["URL"]["url"]
                return original_url

    # Si no se encuentra la URL acortada, devolver un mensaje indicando el error
    return "Short URL no encontrada"

#Ejemplo de uso
#short_url = "https://your-shortening-service.com/1"  # Reemplaza con tu URL acortada
#original_url = get_original_url_from_short_url(short_url)
#print(f"La URL original es: {original_url}")