import requests
import pandas as pd

# ==========================================
NOTION_TOKEN = ""
DATABASE_ID = ""
# ==========================================

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def buscar_existentes():
    existentes = set()
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = requests.post(
            f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
            headers=HEADERS, json=body
        ).json()
        for page in res.get("results", []):
            titulo = page["properties"].get("Company name", {}).get("title", [])
            if titulo:
                existentes.add(titulo[0]["text"]["content"])
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
    return existentes

def numero(valor):
    try:
        v = float(str(valor).replace(",", "."))
        return {"number": None} if pd.isna(v) else {"number": v}
    except:
        return {"number": None}

def select(valor):
    if not pd.notna(valor) or str(valor).strip() == "":
        return {"select": None}
    return {"select": {"name": str(valor)}}

def url(valor):
    if not pd.notna(valor) or str(valor).strip() == "":
        return {"url": None}
    return {"url": str(valor)}

def telefone(valor):
    if not pd.notna(valor) or str(valor).strip() == "":
        return {"phone_number": None}
    return {"phone_number": str(valor)}

def inserir_pagina(row):
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Company name": {"title": [{"text": {"content": str(row["Company name"])}}]},
            "URL":          url(row["URL"]),
            "phone":     telefone(row["phone"]),
        }
    }
    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if res.status_code != 200:
        print(f"  ⚠ Erro em '{row['Company name']}': {res.json().get('message')}")

# ==========================================
print("Lendo arquivo...")
df = pd.read_csv("testclinic2.csv", header=None, names=["Company name", "approaches", "niche", "priority", "URL", "Telefone"], encoding="latin-1")

df = df.dropna(subset=["Company name"])  # remove linhas vazias

print(f"Total de linhas: {len(df)}")

print("Buscando registros existentes no Notion...")
existentes = buscar_existentes()
print(f"Já no Notion: {len(existentes)} registros")

novos = 0
duplicatas = 0

for _, row in df.iterrows():
    nome = str(row["Company name"])
    if nome in existentes:
        duplicatas += 1
        continue
    inserir_pagina(row)
    novos += 1
    print(f"  ✓ {nome}")

print(f"\nPronto! {novos} inseridos, {duplicatas} duplicatas ignoradas.")