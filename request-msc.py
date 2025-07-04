from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import csv

def get_data(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)

    vessel_names = []
    vessel_imo_codes = []

    for vessel in data["vessels"]:
        name = vessel.get("Name")
        imo = vessel.get("LloydsNumber")

        if name and imo:
            vessel_names.append(name)
            vessel_imo_codes.append(imo)
    return vessel_names,vessel_imo_codes

vessel_names,vessel_imo_codes=get_data("active-vessels-msc.json")


def request(L1,L2):
    fichier_csv="msc.csv"

    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        for i,vessel_name in enumerate(L1):
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto("https://www.msc.com/fr/search-a-schedule")
                try:
                    page.locator("button:has-text('Accepter')").click(timeout=5000)
                except:
                    print("Aucun popup cookies détecté (ou déjà accepté).")

                page.locator("button:has-text('Navire')").click()
                page.wait_for_timeout(2000)

                input_selector = "input#vessel"

                page.wait_for_selector(input_selector)
                page.click(input_selector)
                page.fill(input_selector, vessel_name)


                suggestion_selector = 'button[x-on\\:click\\.prevent^="selectVessel"]'
                page.wait_for_selector(suggestion_selector, timeout=5000)
                page.click(suggestion_selector)

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")

                page.wait_for_timeout(5000)

                # Récupérer tous les noms de ports visibles
                port_elements = page.locator('span.data-value.text-capitalize[x-text^="entry.PortName"]')
                ports = port_elements.all_inner_texts()

                print("Ports trouvés :")
                for port in ports:
                    print(port)

                # Récupérer tous les ISO codes affichés
                iso_elements = page.locator('span.data-subheading__iso-code')
                iso_codes = iso_elements.all_inner_texts()

                print("Codes ISO trouvés :")
                for code in iso_codes:
                    print(code)
                writer.writerow(['msc',None,None,iso_codes,ports,None,vessel_name,L2[i]])


                browser.close()

request(vessel_names,vessel_imo_codes)