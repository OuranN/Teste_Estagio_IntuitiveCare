import pandas as pd

def normalize(col):
    return col.strip().lower().replace("_", "").replace(" ", "")

def enriquecer(path_despesas, path_operadoras, path_out):
    despesas = pd.read_csv(path_despesas, dtype={"CNPJ": str})
    despesas["CNPJ"] = despesas["CNPJ"].str.zfill(14)

    oper = pd.read_csv(path_operadoras, sep=";", encoding="utf-8", dtype=str)

    # Normaliza colunas do CADOP
    oper.columns = [normalize(c) for c in oper.columns]

    # Detecta colunas reais
    cnpj_col = "cnpj"
    registro_col = [c for c in oper.columns if "registro" in c][0]
    modalidade_col = [c for c in oper.columns if "modalidade" in c][0]
    uf_col = [c for c in oper.columns if c == "uf"][0]
    data_col = [c for c in oper.columns if "dataregistro" in c][0]

    oper["CNPJ"] = oper[cnpj_col].str.zfill(14)
    oper["DataRegistro"] = pd.to_datetime(oper[data_col], errors="coerce")

    # Mantém o cadastro mais recente por CNPJ
    oper = oper.sort_values("DataRegistro", ascending=False)
    oper = oper.drop_duplicates("CNPJ")

    oper = oper[["CNPJ", registro_col, modalidade_col, uf_col]]
    oper.columns = ["CNPJ", "RegistroANS", "Modalidade", "UF"]

    # Join
    df = despesas.merge(oper, on="CNPJ", how="left")

    # Tratamento de falhas
    df["RegistroANS"] = df["RegistroANS"].fillna("DESCONHECIDO")
    df["Modalidade"] = df["Modalidade"].fillna("DESCONHECIDA")
    df["UF"] = df["UF"].fillna("NA")

    df.to_csv(path_out, index=False)
    return df