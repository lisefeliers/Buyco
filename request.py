import requests
import csv
import time
import random

cosco_vessels = [
    "COSCO AAA",
    "COSCO ADEN",
    "COSCO AFRICA",
    "COSCO AMERICA",
    "COSCO ANTWERP",
    "COSCO AQABA",
    "COSCO ASHDOD",
    "COSCO ASIA",
    "COSCO ATLANTIC",
    "COSCO AUCKLAND",
    "COSCO BELGIUM",
    "COSCO BOSTON",
    "COSCO BREMERHAVEN",
    "COSCO BRISBANE",
    "COSCO BUSAN",
    "COSCO CAPE TOWN",
    "COSCO CHINA",
    "COSCO CHIWAN",
    "COSCO COLOMBO",
    "COSCO DALIAN",
    "COSCO DENMARK",
    "COSCO DEVELOPMENT",
    "COSCO DURBAN",
    "COSCO ENGLAND",
    "COSCO EUROPE",
    "COSCO EXCELLENCE",
    "COSCO FAITH",
    "COSCO FELIXSTOWE",
    "COSCO FORTUNE",
    "COSCO FOS",
    "COSCO FRANCE",
    "COSCO FUKUYAMA",
    "COSCO GENOA",
    "COSCO GERMANY",
    "COSCO GLORY",
    "COSCO HAIFA",
    "COSCO HAMBURG",
    "COSCO HARMONY",
    "COSCO HELLAS",
    "COSCO HONG KONG",
    "COSCO HOPE",
    "COSCO HOUSTON",
    "COSCO INDIAN OCEAN",
    "COSCO INDONESIA",
    "COSCO ISTANBUL",
    "COSCO ITALY",
    "COSCO IZMIR",
    "COSCO JAPAN",
    "COSCO JEDDAH",
    "COSCO KAOHSIUNG",
    "COSCO KARACHI",
    "COSCO KIKU",
    "COSCO KOREA",
    "COSCO LIANYUNGANG",
    "COSCO MALAYSIA",
    "COSCO NAPOLI",
    "COSCO NETHERLANDS",
    "COSCO NEW YORK",
    "COSCO NEWYORK",
    "COSCO NO1",
    "COSCO NORFOLK",
    "COSCO OCEANIA",
    "COSCO PACIFIC",
    "COSCO PANAMA",
    "COSCO PHILIPPINES",
    "COSCO PIRAEUS",
    "COSCO PORTUGAL",
    "COSCO PRIDE",
    "COSCO PRINCE RUPERT",
    "COSCO QINGDAO",
    "COSCO RAN",
    "COSCO REDSEA",
    "COSCO ROTTERDAM",
    "COSCO SAKURA",
    "COSCO SANTOS",
    "COSCO SAO PAULO",
    "COSCO SHANGHAI",
    "COSCO SHEKOU",
    "COSCO SHIPPING ALPS",
    "COSCO SHIPPING ANDES",
    "COSCO SHIPPING AQUARIUS",
    "COSCO SHIPPING ARGENTINA",
    "COSCO SHIPPING ARIES",
    "COSCO SHIPPING AZALEA",
    "COSCO SHIPPING BRAZIL",
    "COSCO SHIPPING CAMELLIA",
    "COSCO SHIPPING CAPRICORN",
    "COSCO SHIPPING CHANG QING",
    "COSCO SHIPPING CHANG SHENG",
    "COSCO SHIPPING CHILE",
    "COSCO SHIPPING DANUBE",
    "COSCO SHIPPING DENALI",
    "COSCO SHIPPING FAN RONG",
    "COSCO SHIPPING FEEDER 1",
    "COSCO SHIPPING FEEDER 2",
    "COSCO SHIPPING FEEDER 3",
    "COSCO SHIPPING FOUNTAIN",
    "COSCO SHIPPING GALAXY",
    "COSCO SHIPPING GEMINI",
    "COSCO SHIPPING GLORY",
    "COSCO SHIPPING GRACE",
    "COSCO SHIPPING HARMONY",
    "COSCO SHIPPING HIMALAYAS",
    "COSCO SHIPPING HONOR",
    "COSCO SHIPPING JASMINE",
    "COSCO SHIPPING JI XIANG",
    "COSCO SHIPPING KILIMANJARO",
    "COSCO SHIPPING LEO",
    "COSCO SHIPPING LIBRA",
    "COSCO SHIPPING LOTUS",
    "COSCO SHIPPING MEXICO",
    "COSCO SHIPPING NEBULA",
    "COSCO SHIPPING ORCHID",
    "COSCO SHIPPING PENG BO",
    "COSCO SHIPPING PENG CHENG",
    "COSCO SHIPPING PEONY",
    "COSCO SHIPPING PERU",
    "COSCO SHIPPING PISCES",
    "COSCO SHIPPING PLANET",
    "COSCO SHIPPING RHINE",
    "COSCO SHIPPING ROSE",
    "COSCO SHIPPING SAGITTARIUS",
    "COSCO SHIPPING SAKURA",
    "COSCO SHIPPING SCORPIO",
    "COSCO SHIPPING SEINE",
    "COSCO SHIPPING SINCERE",
    "COSCO SHIPPING SOLAR",
    "COSCO SHIPPING STAR",
    "COSCO SHIPPING TAURUS",
    "COSCO SHIPPING TENG DA",
    "COSCO SHIPPING THAMES",
    "COSCO SHIPPING UNIVERSE",
    "COSCO SHIPPING URUGUAY",
    "COSCO SHIPPING VIRGO",
    "COSCO SHIPPING VISION",
    "COSCO SHIPPING VOLGA",
    "COSCO SHIPPING WISDOM",
    "COSCO SHIPPING XING WANG",
    "COSCO SHIPPING YANGPU",
    "COSCO SHIPPING ZHUO YUE",
    "COSCO SINGAPORE",
    "COSCO SPAIN",
    "COSCO SURABAYA",
    "COSCO SYDNEY",
    "COSCO TAICANG",
    "COSCO THAILAND",
    "COSCO TIANJIN",
    "COSCO VALENCIA",
    "COSCO VANCOUVER",
    "COSCO VENICE",
    "COSCO VIETNAM",
    "COSCO WELLINGTON",
    "COSCO XIAMEN",
    "COSCO YANTIAN",
    "COSCO YOKOHAMA"
]

cosco_vessels_code=[
  "CZ1", "COF", "COZ", "CCF", "CJB", "CJC", "CJD", "CJE", "CJF", "CJG", "CJH", "CJI", "CJJ",
  "CJK", "CJL", "CJM", "CJN", "CJP", "CJQ", "CJX", "TCA", "TCC", "TCD", "TCE", "TCF", "TCG",
  "TCH", "TCI", "TCJ", "TCK", "TCL", "TCM", "TCN", "TCO", "TCP", "TCQ", "TCR", "TCS", "TCT",
  "TCU", "TCV", "TCW", "TCX", "TCY", "TCZ", "TFA", "TFB", "TFC", "TFD", "TFE", "TFF", "TFG",
  "TFH", "TFI", "TFJ", "TFK", "TFL", "TFM", "TFN", "TFO", "TFP", "TFQ", "TFR", "TFS", "TFT",
  "TFU", "TFV", "TFW", "TFX", "TFY", "TFZ", "TTT", "TAA", "TAH", "TAI", "TAJ", "TAP", "TAO",
  "TAQ", "TAR", "TAS", "TAV", "TAX", "TAY", "TAZ", "151", "152", "153", "T01", "T05", "T06",
  "T07", "T11", "T12", "T22", "T27", "T29", "T33", "T34", "T37", "T38", "T39", "T41", "T42",
  "T54", "T55", "T56", "T80", "T82", "T83", "T91", "T92", "T93", "T94", "T95", "M67", "M69",
  "M83", "M84", "MGG", "MFJ", "MZF", "N9A", "D24", "D3B", "D43", "D44", "D70", "DA8", "DAW",
  "DCP", "SWW", "S1X", "CAN", "CAP", "CAQ", "CAR", "CAS", "CAT", "CAU", "CAV", "CBG", "CBH",
  "CBI", "CBJ", "CBK", "CBL", "CBM", "CBN", "CBO", "CBR", "CBS", "CBT", "CBU", "CBV", "CBW",
  "CBX", "CBZ", "CCG", "CCH", "CCI", "CCJ", "CCK", "CCL", "CCM", "CCN", "CCP", "CCQ", "CCR",
  "CCS", "CCT", "CCU", "CCZ", "CFA", "CFB", "CFC", "CFD", "CFE", "CFF", "CFG", "CFH", "CFI",
  "CFJ", "CKA", "CNB", "CNC", "CND", "CNE", "CNF", "CNT", "COE", "CSB", "CSC", "CSD", "CSE",
  "CSF", "CSG", "CSH", "CSI", "CSJ", "CSK"
]
def request(L1,L2):
    fichier_csv="cosco.csv"

    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)

        for i,vessel_code in enumerate(L2):
            url = f"https://elines.coscoshipping.com/ebschedule/public/purpoShipment/vesselCode?vesselCode={vessel_code}&period=28"
            headers = {"User-Agent": "Mozilla/5.0","Accept": "application/json"}

            response = requests.get(url, headers=headers,timeout=1)
            time.sleep(random.uniform(9, 11))

            if response.status_code == 200:
                Ports=[]
                try:
                    data = response.json()
                    escales = data["data"]["content"]["data"]
                    
                    for escale in escales:
                        port = escale.get("protName")
                        Ports.append(f"{port}")
                        print(f"{port}")
                    writer.writerow(['cosco',None,None,None,Ports,None,L1[i],vessel_code])
                except Exception as e:
                    print(f"Erreur de parsing : {e}")
                    writer.writerow(['cosco',None,None,None,'Error',None,L1[i],vessel_code])
                    time.sleep(10)
            else:
                print(f"Erreur HTTP {response.status_code}")
                writer.writerow(['cosco',None,None,None,'Error',None,L1[i],vessel_code])
                time.sleep(60)


request(cosco_vessels,cosco_vessels_code)