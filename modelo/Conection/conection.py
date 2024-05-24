import requests
from datetime import datetime, timezone
import binascii

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

TOKEN_FOR_NOTION = "secret_PEF343ZLjwQiHRqomIL67F1gaCuo4iksw7sYoK3ZxFn"
TABLE_URL_FOR_USERS = "fa4cf4991442476798e83063c5983fc0"
TABLE_USER = "7ab0e7992dff4e77a8501642636730d5"
TABLE_DETECTED_PSH_URL = "1b70a4030dc34db891b8a6845a9e0fa3"

headers = {
    "Authorization": "Bearer " + TOKEN_FOR_NOTION,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

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

def Consult_data_from_TABLE_DETECTED_PSH_URL():
    url = f"https://api.notion.com/v1/databases/{TABLE_DETECTED_PSH_URL}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # No es necesario guardar los resultados en un archivo JSON
    # with open('db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results

def get_latest_url_id():
    # Consultar los datos de la tabla URL_FOR_USERS
    urls = Consult_data_from_TABLE_URL_FOR_USERS()

    # Encontrar el último URL_ID utilizado
    latest_url_id = 0
    for url in urls:
        url_id = int(url["properties"]["URL_ID"]["title"][0]["text"]["content"])
        latest_url_id = max(latest_url_id, url_id)

    return latest_url_id

def Acortar_URL(url_acortar):
    return base62_encode(binascii.crc32(url_acortar.encode()))

def Create_new_URL(URL):
    # Generar el próximo URL_ID
    next_url_id = get_latest_url_id() + 1

    # Generar una URL acortada
    # Aquí puedes usar un servicio de acortamiento de URL o crear tu propio esquema de acortamiento
    short_url = f"http:/localhost:3000/{Acortar_URL(URL)}"  # Reemplaza esto con tu lógica de acortamiento de URL

    # Crear un nuevo registro de URL en la tabla TABLE_URL_FOR_USERS
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": TABLE_URL_FOR_USERS},
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

#URL = "https://www.ejemplo.com"
#URL1 = "https://www.asdsadsadsa.com"
#URL2 = "https://www.nan.com"
#print(Create_new_URL(URL))
#print(Create_new_URL(URL1))
#print(Create_new_URL(URL2))

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