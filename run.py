from src.downloader import download_last_3_zips
from src.extractor import extract_all_zips
from src.parser import extract_expenses
from src.operators import download_operadoras
from src.consolidator import consolidate
from src.validation import validar
from src.enrichment import enriquecer
from src.aggregation import agregar
import os

# === TESTE 1 ===
download_last_3_zips()
extract_all_zips()
extract_expenses()
download_operadoras()
consolidate()

# === TESTE 2 ===
os.makedirs("data/test2", exist_ok=True)

validar(
    "data/test1/final/consolidado_despesas.csv",
    "data/test2/despesas_validadas.csv"
)

enriquecer(
    "data/test2/despesas_validadas.csv",
    "data/test1/raw/operadoras.csv",
    "data/test2/despesas_enriquecidas.csv"
)

agregar(
    "data/test2/despesas_enriquecidas.csv",
    "data/test2/despesas_agregadas.csv"
)


print("Teste 2 concluído")