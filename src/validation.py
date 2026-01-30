import pandas as pd

def validar_cnpj(cnpj):
    if not isinstance(cnpj, str):
        return False

    cnpj = "".join(filter(str.isdigit, cnpj)).zfill(14)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1

    def calc_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    d1 = calc_digito(cnpj[:12], pesos1)
    d2 = calc_digito(cnpj[:12] + d1, pesos2)

    return cnpj[-2:] == d1 + d2


def validar(path_in, path_out):
    df = pd.read_csv(path_in, dtype={"CNPJ": str})

    df["CNPJ"] = df["CNPJ"].str.zfill(14)

    df["cnpj_valido"] = df["CNPJ"].apply(validar_cnpj)
    df["valor_valido"] = df["ValorDespesas"] > 0
    df["razao_valida"] = df["RazaoSocial"].notna() & (df["RazaoSocial"].str.strip() != "")

    df.to_csv(path_out, index=False)
    return df