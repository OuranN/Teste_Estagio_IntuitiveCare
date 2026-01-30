import pandas as pd

def load_operadoras(path):
    df = pd.read_csv(path, sep=";", encoding="utf-8", dtype=str)

    df = df.rename(columns={
        "CNPJ": "cnpj",
        "Razao_Social": "razao"
    })

    return df[["cnpj", "razao"]]