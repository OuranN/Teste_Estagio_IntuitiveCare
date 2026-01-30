import pandas as pd

def agregar(path_in, path_out):
    df = pd.read_csv(path_in)

    grouped = (
        df.groupby(["RazaoSocial", "UF"])
        .agg(
            TotalDespesas=("ValorDespesas", "sum"),
            MediaTrimestral=("ValorDespesas", "mean"),
            DesvioPadrao=("ValorDespesas", "std"),
            QtdRegistros=("ValorDespesas", "count")
        )
        .reset_index()
    )

    grouped.to_csv(path_out, index=False)
    return grouped