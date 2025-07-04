# Buyco

### a) 
Buyco est une plateforme d'expédition de conteneurs pour chargeurs. Afin de répondre aux besoins des clients, la plateforme doit analyser les différents carrieurs qui permettent d'aller d'un point A à un point B et en combien de temps. Pour ça, elle s'informe sur les sites des différentes compagnies de transport maritime. Elle cherche donc a créer une base de donnéees regroupant toutes les informations nécessaires pour y avoir accès rapidement. La base de données doit aussi se mettre à jour régulièrement pour ne pas donner de fausses informations. Il faut donc : créer cette base de données et récupérer les informations sur les sites pour la remplir, ces informations peuvent être sous la forme de PDF, CSV, API ou autre.

### b) 
### Extraction des informations des sites :  

Pour ce qui est des requêtes POST, nous avons eu l'idée d'utiliser le module request sous python. Mais certains sites stockent tout en front end il n'y a pas de request POST qui va s'addresser au back. On a donc contourner ce problème par plusieurs moyens différents selon les sites.

### Extraction des informations des fichiers (PDF) : 
Nous nous sommes attardés sur les données de CMA CGM qui sont sous format PDF : les données qui nous intéressent sont dans des tableaux de la deuxième page. Nous avons décidé d'utiliser un LLM : d'abord on passe l'ensemble du PDF en Markdown que l'on donne ensuite au LLM pour qu'il nous retourne les données importantes dans la structure d'un tableau au format CSV. 

### Base de données :   

Nous avons commencé par uniquement installer des extensions sur vscode ainsi que mysql Workbench. Après avoir rencontré plusieurs difficultés, Nous avons décidé d'installer un server MySQL local. Pour communiquer avec la db, les requêtes SQL directement via le Workbench ne fonctionnaient pas. Nous avons donc prit la décision de communiquer avec la db sous python via le module SQLAlchemy. Il y a un script de création de table et un script ou on insert les données dans la database. Les données sont bien dans la database , ou peut même le vérifier par le Workbench 
ATTENTION: Le code ne fonctionne que sur mon PC car la database est en local (vous voyez par ailleurs mon mot de passe en clair). Si vous voulez exec le code, il faut créer un serveur local en modifiant quelques lignes.


### c) 
- pdfplumber : 0.11.7
- requests : 2.32.3
- pypdf : 5.7.0
- sqlalchemy : 2.0.39
- sqlalchemy.orm : 1.2.10

### d)

