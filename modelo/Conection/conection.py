
import requests
from datetime import datetime, timezone
import json

TOKEN_FOR_NOTION = "secret_PEF343ZLjwQiHRqomIL67F1gaCuo4iksw7sYoK3ZxFn"
TABLE_URL_FOR_USERS="fa4cf4991442476798e83063c5983fc0" 
TABLE_USER="7ab0e7992dff4e77a8501642636730d5" 
TABLE_DETECTED_PSH_URL="1b70a4030dc34db891b8a6845a9e0fa3"

headers = {
    "Authorization": "Bearer " + TOKEN_FOR_NOTION,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
def safe_get(data, dot_chained_keys):

    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data

def Consult_data_from_TABLE_URL_FOR_USERS():
    url = f"https://api.notion.com/v1/databases/{TABLE_URL_FOR_USERS}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump (data, f, ensure_ascii=False, indent=4)
    
    results = data['results']
   
    return results 

def Consult_data_from_TABLE_USER():
    url = f"https://api.notion.com/v1/databases/{TABLE_USER}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump (data, f, ensure_ascii=False, indent=4)
    
    results = data["results"]
    datos_conseguidos=[]

    for entry in results:
        columna_correo = safe_get(entry, 'properties.correo.rich_text.text.content')
        columna_nombre_Usuario = safe_get(entry, 'properties.nombre_Usuario.text.content')
        columna_password = safe_get(entry, 'properties.password.rich_text.text.content')
        datos_conseguidos.append((columna_correo, columna_nombre_Usuario, columna_password))	
    print (datos_conseguidos)   
    return results 

def Consult_data_from_TABLE_DETECTED_PSH_URL():
    url = f"https://api.notion.com/v1/databases/{TABLE_DETECTED_PSH_URL}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump (data, f, ensure_ascii=False, indent=4)
    
    results = data["results"]
    return results 

test = Consult_data_from_TABLE_USER()