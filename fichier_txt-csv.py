import re
import json
import csv


input_file = "test.txt"
response_file = "test_response.txt"
output_file = "test_table.csv"

# Traitement du fichier .txt donné en réponse par le LLM
responses = []
with open(input_file, "r", encoding="utf-8") as text_file:
    for line in text_file:
        try:
            obj = json.loads(line.strip())
            if "response" in obj:
                responses.append(obj["response"])
        except json.JSONDecodeError:
            continue

full_text = "".join(responses)
full_text = full_text.replace('"""', '').replace('"', '')

with open(response_file, "w", encoding="utf-8") as file:
    file.write(full_text)


# Conversion du fichier .txt amélioré en fichier .csv
lines = [line.strip() for line in full_text.strip().splitlines() if line.strip()]

with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    for line in lines:
        writer.writerow(line.split(","))



# Vérification que le model LLM n'invente pas des données et fais simplement de l'extraction de données
# Faire un test de vérification