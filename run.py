from src.downloader import download_last_3_zips
from src.extractor import extract_all_zips
from src.parser import extract_expenses
from src.operators import download_operadoras
from src.consolidator import consolidate

download_last_3_zips()
extract_all_zips()
extract_expenses()
download_operadoras()
consolidate()
