import requests
from bs4 import BeautifulSoup

url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/"

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)

print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

for a in soup.find_all("a"):
    print(a.get("href"))
