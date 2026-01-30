import os
import pandas as pd
from io import StringIO
from src.expense_filter import is_expense

EXTRACTED_DIR = "data/test1/extracted"
PROCESSED_DIR = "data/test1/processed"

COLS = ["data", "cnpj", "codigo", "descricao", "valor1", "valor2"]

def read_csv(path):
    with open(path, "rb") as f:
        raw = f.read()

    text = raw.decode("utf-8", errors="ignore")

    return pd.read_csv(
        StringIO(text),
        sep=";",
        header=None,
        names=COLS,
        dtype=str
    )



# Extrai apenas Despesas com Eventos / Sinistros de todos os arquivos

def extract_expenses():
    all_expenses = []

    for file in os.listdir(EXTRACTED_DIR):
        if file.endswith(".csv"):
            print("Lendo", file)
            path = os.path.join(EXTRACTED_DIR, file)

            df = read_csv(path)

            # Remove linhas totalmente vazias
            df = df.dropna(how="all")

            # Filtra apenas linhas que são Despesas com Eventos / Sinistros
            df = df[df.apply(is_expense, axis=1)]

            # Extrai ano e trimestre pelo nome do arquivo (ex: 1T2025.csv)
            df["ano"] = file[-8:-4]
            df["trimestre"] = file[0:2]

            all_expenses.append(df)

    # Junta todos os trimestres
    final = pd.concat(all_expenses, ignore_index=True)

    # Normaliza valores monetários

    final["valor1"] = final["valor1"].str.replace(".", "", regex=False).str.replace(",", ".")
    final["valor2"] = final["valor2"].str.replace(".", "", regex=False).str.replace(",", ".")

    final["valor1"] = final["valor1"].astype(float)
    final["valor2"] = final["valor2"].astype(float)

    # Usa valor1 se existir, senão valor2
    final["valor"] = final.apply(
        lambda x: x["valor1"] if x["valor1"] != 0 else x["valor2"],
        axis=1
    )

    # Mantém apenas colunas finais
    final = final[["data", "cnpj", "codigo", "descricao", "valor", "ano", "trimestre"]]

   
    # Salvar arquivo
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    final.to_csv("data/test1/processed/despesas_sinistros.csv", index=False, encoding="utf-8")

    print("Arquivo final salvo em: data/processed/despesas_sinistros.csv")
    print("Total de registros:", len(final))

    return final
