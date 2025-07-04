# Buyco

### a) 
Buyco est une plateforme d'expédition de conteneurs pour chargeurs. Afin de répondre aux besoins des clients, la plateforme doit analyser les différents carrieurs qui permettent d'aller d'un point A à un point B et en combien de temps. Pour ça, elle s'informe sur les sites des différentes compagnies de transport maritime. Elle cherche donc a créer une base de donnéees regroupant toutes les informations nécessaires pour y avoir accès rapidement. La base de données doit aussi se mettre à jour régulièrement pour ne pas donner de fausses informations. Il faut donc : créer cette base de données et récupérer les informations sur les sites pour la remplir, ces informations peuvent être sous la forme de PDF, CSV, API ou autre.

### b) 
### Extraction des informations des sites :  

Pour ce qui est des requêtes POST, nous avons eu l'idée d'utiliser le module request sous python. Mais certains sites stockent tout en front end il n'y a pas de request POST qui va s'addresser au back. On a donc contourner ce problème par plusieurs moyens différents selon les sites.

Sur le site de COSCO on arrive à trouver en inspectant le site l'appel à l'API. On récupère alors ce lien et on peut directement récupérer le résultat de cette requête en faisant une requête GET en python. Le résultat est sous la forme d'un JSON qu'on peut exploiter facilement. Le problème majeur est que nos requêtes sont vites bloquées même si on ajoute des délais randoms.

Un autre type d'extraction utilisé pour les sites de MSC et de Maerks est l'utilisation de la librairie Playwright. On simule un vrai navigateur pour récupèrer le contenu affiché dynamiquement par les sites. C'est un procédé assez long et qui ne se généralise pas à tous les sites facilement. Pourtant il est efficace et semble permettre de faire plus de requête. Un simple appel d'API n'est pas possible car leur API est bloqué.

Pour généraliser aux 10 plus gros armateurs il faut prendre en compte les particularités des autres sites. Certains présentes des fichiers excel pour chaque service, donc facilement exploitable. D'autres mettent en place des captchas qui bloquent toutes tentatives peu sophistiquées de scraping. Certains ont un système de requête par destinations de départ et d'arrivée ce qui implique de modifier la logique de nos codes précédents.

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

Il faut exécuter le notebook 'projet-final.ipynb' qui ira chercher les pdfs dans le dossier 'pdfs'.
Les codes qui permettent de récupérer les fichiers des sites des transporteurs ont un très grand temps d'exécution. Ils ne sont donc pas dans le notebook, mais dans 'extraction-pdf.ipynb'.

