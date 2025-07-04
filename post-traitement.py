import csv
import json

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

def post_traitement():

    # Fichier source et destination
    input_file = "msc.csv"
    output_file = "msc_bis.csv"

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
        open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for i,row in enumerate(reader):
            row[6] = vessel_names[i]
            writer.writerow(row)
            

post_traitement()