import requests
import pandas as pd



NOTION_TOKEN = "NOTION_TOKEN"
DATABASE_ID = "35e901e631288059b12bd763d4ed9d03"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}



def buscar_existentes():
    existentes, cursor = set(), None
    while True:
        body = {"page_size": 100, **({"start_cursor": cursor} if cursor else {})}
        res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=HEADERS, json=body).json()
        for page in res.get("results", []):
            t = page["properties"].get("Company name", {}).get("title", [])
            if t: existentes.add(t[0]["text"]["content"])
        if not res.get("has_more"): break
        cursor = res.get("next_cursor")
    return existentes

def inserir_pagina(row, clinica):
    nome = str(row["Company name"]) if pd.notna(row["Company name"]) else ""
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Company name": {"title": [{"text": {"content": nome}}]},
            "URL":   {"url": clinica.url},
            "phone": {"phone_number": clinica.phone},
        }
    }
    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if res.status_code != 200:
        print(f"  ⚠ '{nome}': {res.json().get('message')}")