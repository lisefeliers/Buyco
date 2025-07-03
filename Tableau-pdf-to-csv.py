import pdfplumber
import shlex
import requests
import re
import json
import csv



# Conversion pdf en Markdown

input_file = "pdfs/ALGA.pdf" 
output_file = "ALGA.md" 

def pdf_tables_to_markdown(pdf_path, output_md):
    with pdfplumber.open(pdf_path) as pdf, open(output_md, "w", encoding="utf-8") as f:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            print(f"Page {page_num}: {len(tables)} tables détectées")
            for i, table in enumerate(tables, 1):
                if not table or not table[0]:
                    continue  
                md = ""
                # En-tête Markdown
                md += "| " + " | ".join(cell if cell is not None else "" for cell in table[0]) + " |\n"
                md += "| " + " | ".join(["---"] * len(table[0])) + " |\n"
                # Lignes du tableau
                for row in table[1:]:
                    md += "| " + " | ".join(cell if cell else "" for cell in row) + " |\n"
                md += "\n\n"  # Ajoute 2 lignes vides entre chaque tableau pour bien séparer
                f.write(md)

pdf_tables_to_markdown(input_file, output_file)



# Extraction des tableaux à l'aide de la plateforme de LLM

input_file = "ALGA.md"
output_file = "ALGA.txt" 

with open(input_file, "r", encoding="utf-8") as f:
    markdown_content = f.read()


prompt_LLM = f"""This is a Markdown file. Extract only table and give them back to me on a readable
 .csv format. Don't comment and don't repharse. Above all else, dont add information from outside the Markdown
file ; Markdown : {markdown_content}""" #Transit Times'
safe_prompt_LLM = shlex.quote(prompt_LLM)

url = "http://ollama-sam.inria.fr/api/generate"
data = {'model': 'mistral:7b', 'prompt': safe_prompt_LLM}
auth = ('Bob', 'hiccup')  # HTTP Basic Auth

response = requests.post(url, json=data, auth=auth)

with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write(response.text)




# Traitement du fichier .txt donné en réponse par le LLM
input_file = "ALGA.txt"
response_file = "ALGA_response.txt"
output_base = "ALGA_table"


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

raw_tables = re.split(r'\n\s*\n', full_text.strip())

for i, table_text in enumerate(raw_tables, 1):
    table_text_clean = table_text.replace("```", "").strip()
    lines = [line.strip() for line in table_text_clean.strip().splitlines() if line.strip()]
    output_file = f"{output_base}_{i}.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, escapechar='\\')
        for line in lines:
            writer.writerow(line.split(","))

    print(f"Table {i} saved in {output_file}") 



# Vérification que le model LLM n'invente pas des données et fais simplement de l'extraction de données
# Faire un test de vérification