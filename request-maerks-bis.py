from playwright.sync_api import sync_playwright
import csv
import json


def get_data(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)

    vessel_names = []
    vessel_maersk_codes = []
    vessel_imo_codes = []

    for vessel in data["vessels"]:
        name = vessel.get("vesselName")
        code = vessel.get("vesselMaerskCode")
        imo = vessel.get("vesselIMONumber")

        if name and code and imo:
            vessel_names.append(name)
            vessel_maersk_codes.append(code)
            vessel_imo_codes.append(imo)
    return vessel_names, vessel_maersk_codes, vessel_imo_codes


def request_playwright(L1, L2, L3):
    fichier_csv = "maersk.csv"

    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        writer.writerow(['compagnie', 'port1', 'port2', 'port3', 'liste_ports', 'imo', 'nom_navire', 'code_maersk'])

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for i, vessel_code in enumerate(L2):
                url = f"https://www.maersk.com/schedules/vesselSchedules?vesselCode={vessel_code}&fromDate=2025-07-05"
                print(f"🔍 Chargement : {url}")
                try:
                    page.goto(url, timeout=3000)
                    page.wait_for_timeout(4000)  # attendre que JS ait fini

                    # 🔎 Extraire les textes des liens pertinents
                    ports = page.locator("a[href*='fromDate=2025-07-05']").all_inner_texts()

                    writer.writerow(['maersk', None, None, None, ports, L3[i], L1[i], vessel_code])

                except Exception as e:
                    print(f"❌ Erreur sur {vessel_code} - {L1[i]} : {e}")
                    writer.writerow(['maersk', None, None, None, 'Error', L3[i], L1[i], vessel_code])

            browser.close()


# Chargement des données
vessel_names, vessel_maersk_codes, vessel_imo_codes = get_data("active-vessels-maerks.json")

# Exécution
request_playwright(vessel_names, vessel_maersk_codes, vessel_imo_codes)
