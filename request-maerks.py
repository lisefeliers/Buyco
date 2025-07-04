import requests
import time
import random
import json
import csv
from bs4 import BeautifulSoup


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
    return vessel_names,vessel_maersk_codes,vessel_imo_codes



vessel_names,vessel_maersk_codes,vessel_imo_codes=get_data("active-vessels-maerks.json")

def request(L1,L2,L3):
    fichier_csv="maerks.csv"

    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)

        for i,vessel_code in enumerate(L2):
            url = f"https://www.maersk.com/schedules/vesselSchedules?vesselCode={vessel_code}&fromDate=2025-07-05"
            headers = {"User-Agent": "Mozilla/5.0","Accept": "application/json"}

            response = requests.get(url, headers=headers,timeout=1)
            print(response)
            time.sleep(random.uniform(1, 1.5))

            soup = BeautifulSoup(response.content, "html.parser")
            Ports = [
                a.get_text(strip=True)
                for a in soup.find_all("a", href=True)
                if "fromDate=2025-07-05" in a["href"]
            ]
            writer.writerow(['maerks',None,None,None,Ports,None,L1[i],L3[i]])


request(vessel_names,vessel_maersk_codes,vessel_imo_codes)