import pdfplumber
import shlex
import requests
import re
import json
import csv
from pypdf import PdfReader, PdfWriter


nom_fichier = "extract_AGAPOME_2" # que le nom (sans .pdf)

# Conversion pdf en Markdown

input_file = f"pdfs_extraits\{nom_fichier}.pdf" 
output_file = f"{nom_fichier}.md" 

def pdf_tables_to_markdown(pdf_path, output_md):
    with pdfplumber.open(pdf_path) as pdf, open(output_md, "w", encoding="utf-8") as f:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            print(f"Page {page_num}: {len(tables)} tables détectées")
            for i, table in enumerate(tables, 1):
                if not table or not table[0]:
                    continue  
                md = ""
                md += "| " + " | ".join(cell if cell is not None else "" for cell in table[0]) + " |\n"
                md += "| " + " | ".join(["---"] * len(table[0])) + " |\n"
                for row in table[1:]:
                    md += "| " + " | ".join(cell if cell else "" for cell in row) + " |\n"
                md += "\n\n" 
                f.write(md)

pdf_tables_to_markdown(input_file, output_file)



# Extraction des tableaux à l'aide de la plateforme de LLM

input_file = f"{nom_fichier}.md"
output_file = f"{nom_fichier}.txt" 

with open(input_file, "r", encoding="utf-8") as f:
    markdown_content = f.read()


prompt_LLM = f"""This is a Markdown file. Extract only table and give them back to me on a readable
 .csv format. Don't comment and don't repharse. Above all else, dont add information from outside the Markdown
file. Let the tables how they are in the Markdown. when there is a line feed, it changes tables; Markdown : {markdown_content}""" #Transit Times'
safe_prompt_LLM = shlex.quote(prompt_LLM)

url = "http://ollama-sam.inria.fr/api/generate"
data = {'model': 'mistral:7b', 'prompt': safe_prompt_LLM}
auth = ('Bob', 'hiccup')  # HTTP Basic Auth

response = requests.post(url, json=data, auth=auth)

with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write(response.text)




# Traitement du fichier .txt donné en réponse par le LLM

input_file = f"{nom_fichier}.txt"
response_file = f"{nom_fichier}_response.txt"
output_file = f"{nom_fichier}_table.csv"

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

input_file = f"{nom_fichier}_response.txt"
output_base = f"{nom_fichier}_table"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Extraire contenu entre ```
match = re.search(r"```(.*?)```", content, re.DOTALL)
if not match:
    raise ValueError("Bloc markdown ``` non trouvé dans le fichier de réponse")

tables_text = match.group(1).strip()

lines = [line.strip() for line in tables_text.splitlines() if line.strip()]

# Trouver l'index où la deuxième table commence
split_index = None
prev_len = None
for i, line in enumerate(lines):
    cols = line.split(",")
    if prev_len is not None and len(cols) > prev_len:
        split_index = i
        break
    prev_len = len(cols)

if split_index is None:
    tables = [lines]
else:
    tables = [lines[:split_index], lines[split_index:]]
if len(tables) > 1:
    second_table = tables[1]
    first_line_cols = second_table[0].split(",")
    first_line_cols[0] = "To\nFrom"
    import io
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(first_line_cols)
    tables[1][0] = output.getvalue().strip() 

# Écriture des tables dans des fichiers CSV
for i, table_lines in enumerate(tables, 1):
    output_file = f"{output_base}_{i}.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        for line in table_lines:
            row = next(csv.reader([line]))
            writer.writerow(row)
    print(f"Table {i} saved in {output_file}")