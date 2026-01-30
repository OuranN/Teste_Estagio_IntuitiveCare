import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

RAW_DIR = "data/test1/raw" # Pasta onde os arquivos serao salvos


def list_links(url):
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href and href.endswith(".zip"):
            links.append(href)

    return links


def get_latest_year():
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    years = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href and href.strip("/").isdigit():
            years.append(href.strip("/"))

    years.sort()
    return years[-1]


def download_last_3_zips():
    os.makedirs(RAW_DIR, exist_ok=True)

    year = get_latest_year()
    year_url = urljoin(BASE_URL, year + "/")

    zips = list_links(year_url)
    zips.sort()

    last_3 = zips[-3:]

    downloaded = []

    for zip_name in last_3:
        url = urljoin(year_url, zip_name)
        file_path = os.path.join(RAW_DIR, zip_name)

        print(f"Baixando {zip_name}...")

        r = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(r.content)

        downloaded.append(file_path)

    return downloaded
