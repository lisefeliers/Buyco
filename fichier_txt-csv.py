import re
import json



# Traitement du fichier .txt

input_file = "test.txt" #"WAX_0.txt"
output_file = "test_table1.csv" #"WAX_0_table1.csv"

# Reconstruire le texte complet depuis les fragments JSON
responses = []

with open(input_file, "r", encoding="utf-8") as text_file:
    for line in text_file:
        try:
            obj = json.loads(line.strip())
            if "response" in obj:
                responses.append(obj["response"])
        except json.JSONDecodeError:
            continue  # ignore les lignes malformées (au cas où)

# Concaténer tous les fragments
full_text = "".join(responses)

response_file = "test_response.txt" #"WAX_0_response.txt"

with open(response_file, "w", encoding="utf-8") as file:
    file.write(full_text)

# Création des fichiers .csv

output_base = "test_table" #"WAX_0_table"

csv_blocks = re.findall(r'(?:[^\n]*,[^\n]*\n)+', full_text)

for i, block in enumerate(csv_blocks, start=1):
    output_csv = f"{output_base}{i}.csv"
    with open(output_csv, "w", encoding="utf-8") as f:
        f.write(block)




# Vérification que le model LLM n'invente pas des données et fais simplement de l'extraction de données
# Faire un test de vérification