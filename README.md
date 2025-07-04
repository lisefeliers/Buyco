# Buyco

### a) 
Buyco est une plateforme d'expédition de conteneurs pour chargeurs. Afin de répondre aux besoins des clients, la plateforme doit analyser les différentes carrières qui permettent d'aller d'un point A à un point B et en combien de temps. Pour ça, elle s'informe sur les sites des différentes compagnies de transport maritime. Elle cherche donc a créer une base de donnéees regroupant toutes les informations nécessaires pour y avoir accès rapidement. La base de données doit aussi se mettre à jour régulièrement pour ne pas donner de fausses informations. Il faut donc : créer cette base de données et récupérer les informations sur les sites pour la remplir, ces informations peuvent être sous la forme de PDF, CSV, API ou autre.

### b) 
### Extraction des informations des sites :   

### Extraction des informations des fichiers (PDF) : 
Nous nous sommes attardés sur les données de CMA CGM qui sont sous format PDF : les données qui nous intéressent sont dans des tableaux de la deuxième page. Nous avons décidé d'utiliser un LLM : d'abord on passe l'ensemble du PDF en Markdown que l'on donne ensuite au LLM pour qu'il nous retourne les données importantes dans la structure d'un tableau au format CSV. 

### Base de données :   


### c) 
- pdfplumber : 0.11.7
- requests : 2.32.3
- pypdf : 5.7.0
- sqlalchemy : 2.0.39
- sqlalchemy.orm : 1.2.10

### d)

