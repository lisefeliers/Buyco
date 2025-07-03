from playwright.sync_api import sync_playwright
import json

def search_msc_by_imo(imo: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale="fr-FR")
        page = context.new_page()

        # Stocke la réponse capturée
        captured_response = {}

        def handle_response(response):
            if "SearchLiveSchedule" in response.url and response.status == 200:
                try:
                    data = response.json()
                    captured_response["data"] = data
                except:
                    captured_response["data"] = "Erreur JSON"

        page.on("response", handle_response)

        # Va sur MSC pour obtenir cookies/session
        page.goto("https://www.msc.com/fr", wait_until="networkidle")

        # Envoie la requête via JS dans le contexte navigateur
        page.evaluate(f"""
            fetch("https://www.msc.com/api/feature/tools/SearchLiveSchedule", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{"VesselIMONumber":"{imo}","language":"fr-FR"}})
            }})
        """)

        # Attend 5 secondes pour laisser le temps à la réponse d'arriver
        page.wait_for_timeout(5000)
        browser.close()

        if "data" in captured_response:
            print(json.dumps(captured_response["data"], indent=2, ensure_ascii=False))
        else:
            print("❌ Aucune réponse capturée (possible blocage JS ou CORS)")

# Utilisation
search_msc_by_imo("9229829")
