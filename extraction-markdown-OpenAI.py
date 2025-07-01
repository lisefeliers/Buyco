from markitdown import MarkItDown
from openai import OpenAI
import os


# Conversion pdf en markdown

markitdown = MarkItDown()
result = markitdown.convert("pdfs/WAX_0.pdf")
output_file = "WAX_0.md"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(result.text_content)



# Extraction des tableaux à l'aide d'OpenAI

client-CMACGM = OpenAI(api_key=os.getenv("cle-perso-openai"))  

with open(file, "r", encoding="utf-8") as f:
    markdown_content = f.read()

system_prompt = "extraction de données présentes dans des tableaux"
user_prompt = f"""Voici le contenu d'un fichier Markdown. Extrait uniquement les tableaux de temps de transit**
(Transit Times), et rends-les sous forme de tableaux lisibles csv. Ne commente pas, ne reformule pas.
Markdown : {markdown_content}"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un assistant..."},
        {"role": "user", "content": "Voici un fichier markdown..."}
    ]
)

texte = response.choices[0].message.content
print(texte)
