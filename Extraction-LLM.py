import pdfplumber # extraire tableaus depuis fichier pdf
import shlex # protection chaîne de caractère
import requests # envoyer des requêtes HTTP
import re # découper un texte à l'aide d'expressions singulières
import json
import csv




# Conversion pdf en Markdown

name_file = "GTL_0"
input_file = f"pdfs/{name_file}.pdf" 
output_file = f"{name_file}.md" 

def pdf_tables_to_markdown(pdf_path, output_md):
    # lit un fichier pdf avec des tableaux, les extraits et les convertit en markdown pui les auvegarde dans un fichier
    with pdfplumber.open(pdf_path) as pdf, open(output_md, "w", encoding="utf-8") as f:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            print(f"Page {page_num}: {len(tables)} tables détectées")
            for table in tables :
                if not table or not table[0]: # vérifie que le tableau n'ets pas vide et qu'il a une en-tête
                    continue  
                md = ""
                # En-tête Markdown
                md += "| " + " | ".join(cell if cell is not None else "" for cell in table[0]) + " |\n" # .join(sépare les éléments de la liste par " | ")
                md += "| " + " | ".join(["---"] * len(table[0])) + " |\n"
                # Lignes du tableau
                for row in table[1:]:
                    md += "| " + " | ".join(cell if cell else "" for cell in row) + " |\n"
                md += "\n\n"  # Ajoute 2 lignes vides entre chaque tableau pour bien les séparer
                f.write(md)

pdf_tables_to_markdown(input_file, output_file)



# Extraction des tableaux à l'aide de la plateforme de LLM

input_file = f"{name_file}.md"
output_file = f"{name_file}.txt" 

with open(input_file, "r", encoding="utf-8") as f:
    markdown_content = f.read()


prompt_LLM = f"""This is a Markdown file. Extract only table and give them back to me on a readable
 .csv format. ; Markdown : {markdown_content}""" #Transit Times'

safe_prompt_LLM = shlex.quote(prompt_LLM) # évite que le prompt ne soit déformé

url = "http://ollama-sam.inria.fr/api/generate" # adresse où serveur LLM est hébergé
data = {'model': 'mistral:7b', 'prompt': safe_prompt_LLM} # modèle utilisé, prompt
auth = ('Bob', 'hiccup')  # utiliateur et mot de passe d'identification

response = requests.post(url, json=data, auth=auth) # recupère la réponse du LLM

with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write(response.text)



# Traitement du fichier .txt donné en réponse par le LLM

input_file = f"{name_file}.txt"
response_file = f"{name_file}_response.txt"
output_base = f"{name_file}_table"

responses = []

with open(input_file, "r", encoding="utf-8") as text_file:
    for line in text_file:
        try:
            obj = json.loads(line.strip()) # cinvertit la chaîne JSON en dictionnaire python
            if "response" in obj:
                responses.append(obj["response"])
        except json.JSONDecodeError:
            continue

full_text = "".join(responses) # fusionnes les réponses en un seul texte
full_text = full_text.replace('"""', '').replace('"', '') # retire les '''''' et "" pour les remplacer par ''

with open(response_file, "w", encoding="utf-8") as file:
    file.write(full_text)



# Conversion du fichier .txt amélioré en fichier .csv

raw_tables = re.split(r'\n\s*\n', full_text.strip()) # sépare les différents tableaux

for i, table_text in enumerate(raw_tables, 1):
    table_text_clean = table_text.replace("```", "").strip()
    lines = [line.strip() for line in table_text_clean.strip().splitlines() if line.strip()]
    output_file = f"{output_base}_{i}.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, escapechar='\\')
        for line in lines:
            writer.writerow(line.split(",")) # séparateur ,
    print(f"Table {i} saved in {output_file}") 


# Vérification que le model LLM n'invente pas des données et fais simplement de l'extraction de données
# Faire un test de vérification