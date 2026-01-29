import pandas as pd

def load_operadoras(path):
    df = pd.read_csv(path, sep=";", encoding="latin1", dtype=str)

    df = df.rename(columns={
        "CNPJ": "cnpj",
        "Razao_Social": "razao"
    })

    return df[["cnpj", "razao"]]