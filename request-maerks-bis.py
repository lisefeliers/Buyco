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

        with sync_playwright() as p:


            for i, vessel_code in enumerate(L2):
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800},
                java_script_enabled=True,
                locale="fr-FR")

                page = context.new_page()
                url = f"https://www.maersk.com/schedules/vesselSchedules?vesselCode={vessel_code}&fromDate=2025-07-05"
                print(f"Chargement : {url}")
                try:
                    page.goto(url, timeout=20000)
                    page.wait_for_timeout(3000)
                    # Ciblage strict du bon bouton cookie
                    accept_button = page.locator('button[data-test="coi-allow-all-button"]')

                    try:
                        if accept_button.count() > 0:
                            accept_button.evaluate("el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
                            accept_button.click()
                        else:
                            print("Aucun bouton de cookies trouvé.")
                    except Exception as e:
                        print(f"Erreur en cliquant sur le bouton cookie : {e}")

                    # Attendre l'apparition du pop-up
                    page.wait_for_timeout(2000)  # facultatif : donne le temps au pop-up de s'afficher

                    try:
                        got_it_button = page.locator("button:has-text('Got it')")
                        if got_it_button.is_visible():
                            got_it_button.click()
                            page.wait_for_timeout(1000)
                    except Exception as e:
                        print(f"Erreur en fermant le pop-up : {e}")


                    # Attendre que les liens soient rendus
                    page.wait_for_timeout(2000)

                    # Vérifie et récupère les balises <a> ayant le bon lien
                    port_links = page.locator('a')

                    hrefs = port_links.evaluate_all("""
                        (elements) => elements
                            .filter(a => a.href && a.href.startsWith("https://www.maersk.com/schedules/portCalls"))
                            .map(a => a.innerText.trim())
                    """)

                    writer.writerow(['maersk', None, None, None, hrefs, L3[i], L1[i], vessel_code])
                    print('OK')

                except Exception as e:
                    print(f"Erreur sur {vessel_code} - {L1[i]} : {e}")
                    writer.writerow(['maersk', None, None, None, 'Error', L3[i], L1[i], vessel_code])

                browser.close()


# Chargement des données
vessel_names, vessel_maersk_codes, vessel_imo_codes = get_data("active-vessels-maerks.json")

# Exécution
request_playwright(vessel_names, vessel_maersk_codes, vessel_imo_codes)
