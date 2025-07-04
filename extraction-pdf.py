import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time

# URL de la page contenant les liens vers les PDF
url_page = "https://www.cma-cgm.fr/produits-services/plaquettes"

# Dossier de destination pour les PDF téléchargés
os.makedirs("pdfs_bis", exist_ok=True)

# Récupération de la page HTML
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get("https://www.cma-cgm.fr/produits-services/plaquettes", headers=headers)
print(response)
soup = BeautifulSoup(response.content, "html.parser")
count=0

# Recherche de tous les liens PDF
for link in soup.find_all("a", href=True):
    href = link["href"]
    if href.lower().endswith(".pdf"):
        count+=1
        time.sleep(1)
        if count==10:
            count=0
            time.sleep(60)
        pdf_url = urljoin(url_page, href)  # gère les liens relatifs
        pdf_name = os.path.basename(href)
        pdf_path = os.path.join("pdfs_bis", pdf_name)

        print(f"Téléchargement : {pdf_url}")
        with open(pdf_path, "wb") as f:
            f.write(requests.get(pdf_url).content)