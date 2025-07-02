import bash
import subprocess
import shlex
import requests
import re
import json



# Extraction des tableaux à l'aide de la plateforme de LLM

input_file = "test.md" #"WAX_0.md"

with open(input_file, "r", encoding="utf-8") as f:
    markdown_content = f.read()

prompt_LLM_fra = f"""Voici le contenu d'un fichier Markdown. Extrait uniquement les tableaux de temps de transit**
(Transit Times), et rends-les sous forme de tableaux lisibles .csv Ne commente pas, ne reformule pas.
Markdown : {markdown_content}"""

prompt_LLM = f"""This is a Markdown file. Extract only data and give them back to me on a readable
 .csv format. Don't comment and don't repharse. Above all else, do npt add information from outside the Markdown
file ; Markdown : {markdown_content}""" #Transit Times'

safe_prompt_LLM = shlex.quote(prompt_LLM)

output_file = "test.txt" #"WAX_0.txt"

# Methode bash non utilisée finalement

#print(bash.bash(f"""http -F Bob:hiccup@ollama-sam.inria.fr/api/generate model='mistral:7b' prompt='{prompt_LLM}' > text-bis.txt"""))


# Methode subprocess

#cmd = f"""http -F Bob:hiccup@ollama-sam.inria.fr/api/generate model='mistral:7b' prompt={safe_prompt_LLM} """

#with open(output_file, "w", encoding="utf-8") as out_file:
#    subprocess.run(cmd, shell=True, stdout=out_file)

#http -F Bob:hiccup@ollama-sam.inria.fr/api/generate model="mistral:7b" prompt=prompt-LLM


# Méthode requests non utilisée finalement

url = "http://ollama-sam.inria.fr/api/generate"
data = {'model': 'mistral:7b', 'prompt': safe_prompt_LLM}
auth = ('Bob', 'hiccup')  # HTTP Basic Auth

response = requests.post(url, json=data, auth=auth)


with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write(response.text)


