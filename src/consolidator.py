import pandas as pd
import os
import zipfile

def consolidate():
    print("Lendo despesas...")
    df = pd.read_csv("data/test1/processed/despesas_sinistros.csv", dtype=str)

    # O campo "cnpj" nos arquivos de despesas é na verdade o REGISTRO ANS
    df = df.rename(columns={"cnpj": "REGISTRO_OPERADORA"})

    # Normalizar valor
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df[df["valor"] > 0]

    print("Lendo cadastro de operadoras...")
    oper = pd.read_csv("data/test1/raw/operadoras.csv", sep=";", encoding="utf-8", dtype=str)

    oper = oper[["REGISTRO_OPERADORA", "CNPJ", "Razao_Social"]]
    oper = oper.rename(columns={
        "Razao_Social": "RazaoSocial"
    })

    print("Relacionando Registro ANS com operadoras...")
    df = df.merge(oper, on="REGISTRO_OPERADORA", how="left")

    # Tratar operadoras não encontradas
    df["RazaoSocial"] = df["RazaoSocial"].fillna("DESCONHECIDA")
    df["CNPJ"] = df["CNPJ"].fillna("00000000000000")

    print("Consolidando...")
    final = (
        df.groupby(["CNPJ", "RazaoSocial", "ano", "trimestre"], as_index=False)
        .agg(ValorDespesas=("valor", "sum"))
    )

    final = final.rename(columns={
        "ano": "Ano",
        "trimestre": "Trimestre"
    })

    os.makedirs("data/test1/final", exist_ok=True)

    final_path = "data/test1/final/consolidado_despesas.csv"
    final.to_csv(final_path, index=False)

    with zipfile.ZipFile("data/test1/final/consolidado_despesas.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(final_path, arcname="consolidado_despesas.csv")

    print("Arquivo gerado:", final_path)
    print("Total de linhas:", len(final))

    return final


if __name__ == "__main__":
    consolidate()