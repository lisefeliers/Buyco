import csv
from sqlalchemy import create_engine, text

# Connexion à la base de données
engine = create_engine('mysql+pymysql://root:rootinfo8988*Mines@localhost:3306/app', echo=True)

# Lecture du fichier CSV et insertion dans la base
with engine.connect() as con:
    with open('../exemple.csv', 'r', encoding='utf-8') as file:
        lecteur = csv.reader(file)
        
        next(lecteur)  # Ignore l'en-tête

        for ligne in lecteur:
            print(ligne)
            if len(ligne) < 7:
                print("Ligne incomplète :", ligne)
                continue

            id_carrier, code_route, name_route, port_code, port_name, terminal, vessels = ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6]

            # Exemple de requête d'insertion, adapte selon ta table réelle
            query = text("""
                INSERT INTO data (id_carrier, code_route, name_route, port_code, port_name, terminal, vessels)
                VALUES (:id_carrier, :code_route, :name_route, :port_code, :port_name, :terminal, :vessels)
            """)
            con.execute(query, {
                'id_carrier': id_carrier,
                'code_route': code_route,
                'name_route': name_route,
                'port_code': port_code,
                'port_name': port_name,
                'terminal': terminal,
                'vessels': vessels
            })

    con.commit()
