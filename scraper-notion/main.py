import pandas as pd
from model.validation import Clinica
from rds.addcolumn import buscar_existentes,inserir_pagina


# ==========================================
df = pd.read_csv("testclinic2.csv", header=None, names=["Company name", "URL", "phone"], encoding="latin-1")

print(f"Total: {len(df)} linhas — Validando...")
validas = []
for i, (_, row) in enumerate(df.iterrows(), 1):
    try:
        clinica = Clinica(
            company_name=str(row["Company name"]) if pd.notna(row["Company name"]) else None,
            url=str(row["URL"]).strip() if pd.notna(row["URL"]) else None,
            phone=str(row["phone"]).strip() if pd.notna(row["phone"]) else None
        )
        validas.append((row, clinica))
    except Exception as e:
        print(f"  ❌ Linha {i} — {e}")

print(f"✓ {len(validas)} válidas | ❌ {len(df) - len(validas)} erros")
if len(validas) < len(df): exit()

existentes = buscar_existentes()
novos = duplicatas = 0
for row, clinica in validas:
    nome = str(row["Company name"]) if pd.notna(row["Company name"]) else ""
    if nome in existentes:
        duplicatas += 1
    else:
        inserir_pagina(row, clinica)
        novos += 1
        print(f"  ✓ {nome}")

print(f"\nPronto! {novos} inseridos, {duplicatas} duplicatas ignoradas.")