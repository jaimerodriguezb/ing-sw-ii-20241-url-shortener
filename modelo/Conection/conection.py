import requests
from datetime import datetime, timezone
import json
import random
import string

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

def Consult_data_from_TABLE_USER():
    url = f"https://api.notion.com/v1/databases/{TABLE_USER}/query"

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

def Create_new_user(nombre_usuario, correo, password):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": TABLE_USER},
        "properties": {
            "nombre_Usuario": {"title": [{"text": {"content": nombre_usuario}}]},
            "correo": {"rich_text": [{"text": {"content": correo}}]},
            "password": {"rich_text": [{"text": {"content": password}}]},
            "conteo_URL_acortadas": {"rich_text": [{"text": {"content": "0"}}]}  # Convertido a rich_text con "rich_text"
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return "Usuario creado exitosamente"
    else:
        return f"Error al crear usuario: {response.text}"

def Modify_conteo_URL_acortadas(correo, nuevo_conteo):
    users = Consult_data_from_TABLE_USER()
    for user in users:
        if user["properties"]["correo"]["rich_text"][0]["text"]["content"] == correo:
            user_id = user["id"]
            break
    else:
        return "Usuario no encontrado"
    
    url = f"https://api.notion.com/v1/pages/{user_id}"
    payload = {
        "properties": {
            "conteo_URL_acortadas": {"rich_text": [{"text": {"content": str(nuevo_conteo)}}]}  # Convertir a rich_text
        }
    }
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:
        return f"Conteo de URL acortadas modificado correctamente para el usuario con correo {correo}"
    else:
        return f"Error al modificar el conteo de URL acortadas: {response.text}"

def Delete_user_by_email(correo):
    users = Consult_data_from_TABLE_USER()
    for user in users:
        if user["properties"]["correo"]["rich_text"][0]["text"]["content"] == correo:
            user_id = user["id"]
            break
    else:
        return "Usuario no encontrado"
    
    url = f"https://api.notion.com/v1/pages/{user_id}"
    payload = {"archived": True}  # Marcar el usuario como archivado
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:
        return f"Usuario con correo {correo} eliminado correctamente"
    else:
        return f"Error al eliminar el usuario: {response.text}"
    
# Ejemplo de uso
# Crear un nuevo usuario
print(Create_new_user("Ejemplo Usuario", "ejemplo@correo.com", "contraseña123"))

# Modificar el conteo de URL acortadas para un usuario
#print(Modify_conteo_URL_acortadas("ejemplo@correo.com", 10))

# Eliminar un usuario por correo
#print(Delete_user_by_email("ejemplo@correo.com"))

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    return short_url

def get_latest_url_id():
    # Consultar los datos de la tabla URL_FOR_USERS
    urls = Consult_data_from_TABLE_URL_FOR_USERS()

    # Encontrar el último URL_ID utilizado
    latest_url_id = 0
    for url in urls:
        url_id = int(url["properties"]["URL_ID"]["title"][0]["text"]["content"])
        latest_url_id = max(latest_url_id, url_id)

    return latest_url_id

def Create_new_URL(user_email, URL):
    # Obtener el ID del usuario basado en el correo electrónico
    user_id = None
    users = Consult_data_from_TABLE_USER()
    for user in users:
        if user["properties"]["correo"]["rich_text"][0]["text"]["content"] == user_email:
            user_id = user["id"]
            break
    else:
        return "Usuario no encontrado"

    # Obtener el conteo actual de URL acortadas del usuario y aumentarlo en 1
    conteo_URL_acortadas = 0
    if "conteo_URL_acortadas" in user["properties"]:
        conteo_URL_acortadas = int(user["properties"]["conteo_URL_acortadas"]["rich_text"][0]["text"]["content"]) + 1
    else:
        # Si el campo conteo_URL_acortadas no está presente, se considera como 0
        user["properties"]["conteo_URL_acortadas"] = {"rich_text": [{"text": {"content": "0"}}]}

    # Actualizar el conteo de URL acortadas del usuario
    Modify_conteo_URL_acortadas(user_email, conteo_URL_acortadas)

    # Generar el próximo URL_ID
    next_url_id = get_latest_url_id() + 1

    # Generar una URL acortada
    # Aquí puedes usar un servicio de acortamiento de URL o crear tu propio esquema de acortamiento
    short_url = f"https://your-shortening-service.com/{next_url_id}"  # Reemplaza esto con tu lógica de acortamiento de URL

    # Crear un nuevo registro de URL en la tabla TABLE_URL_FOR_USERS
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": TABLE_URL_FOR_USERS},
        "properties": {
            "URL_ID": {"title": [{"text": {"content": str(next_url_id)}}]},
            "User_ID": {"rich_text": [{"text": {"content": user_email}}]},
            "URL": {"url": URL},
            "Short_URL": {"url": short_url},
            "Fecha": {"date": {"start": datetime.now().astimezone(timezone.utc).isoformat()}}
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return "URL creada correctamente"
    else:
        return f"Error al crear la URL: {response.text}"

# Ejemplo de uso
user_email = "ejemplo@correo.com"
URL = "https://www.ejemplo.com"
URL1 = "https://www.asdsadsadsa.com"
print(Create_new_URL(user_email, URL))
print(Create_new_URL(user_email, URL1))

def get_urls_for_user(user_email):
    # Obtener el ID del usuario basado en el correo electrónico
    user_id = None
    users = Consult_data_from_TABLE_USER()
    for user in users:
        if user["properties"]["correo"]["rich_text"][0]["text"]["content"] == user_email:
            user_id = user["id"]
            break
    else:
        return "Usuario no encontrado"

    # Consultar los datos de la tabla URL_FOR_USERS
    urls = Consult_data_from_TABLE_URL_FOR_USERS()

    # Filtrar las URLs asociadas al usuario específico
    user_urls = []
    for url in urls:
        if url["properties"]["User_ID"]["rich_text"][0]["text"]["content"] == user_email:
            user_urls.append({
                "URL_ID": url["properties"]["URL_ID"]["title"][0]["text"]["content"],
                "URL": url["properties"]["URL"]["url"],
                "Short_URL": url["properties"]["Short_URL"]["url"],
                "Fecha": url["properties"]["Fecha"]["date"]["start"]
            })

    return user_urls

# Ejemplo de uso
user_email = "ejemplo@correo.com"
user_urls = get_urls_for_user(user_email)
print("URLs asociadas al usuario:")
for url_data in user_urls:
    print(url_data)