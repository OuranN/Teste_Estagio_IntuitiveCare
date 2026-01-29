import os
import requests

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
DEST = "data/raw/operadoras.csv"

def download_operadoras():
    os.makedirs("data/raw", exist_ok=True)

    url = BASE_URL + "Relatorio_cadop.csv"
    print("Baixando cadastro de operadoras...")

    r = requests.get(url)
    with open(DEST, "wb") as f:
        f.write(r.content)

    return DEST
