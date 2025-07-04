import csv
from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:rootinfo8988*Mines@localhost:3306/app', echo=True)

# csv
with engine.connect() as con:
    with open('../exemple.csv', 'r', encoding='utf-8') as file:
        lecteur = csv.reader(file)
        
        next(lecteur)  

        for ligne in lecteur:
            print(ligne)
            if len(ligne) < 7:
                print("Ligne incomplète :", ligne)
                continue

            name_carrier, code_route, name_route, port_code, port_name, terminal, vessels,vessels_code = ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7]

            
            query = text("""
                INSERT INTO data2 (name_carrier, code_route, name_route, port_code, port_name, terminal, vessels, vessels_code)
                VALUES (:name_carrier, :code_route, :name_route, :port_code, :port_name, :terminal, :vessels, vessels_code)
            """)
            con.execute(query, {
                'id_carrier': name_carrier,
                'code_route': code_route,
                'name_route': name_route,
                'port_code': port_code,
                'port_name': port_name,
                'terminal': terminal,
                'vessels': vessels,
                'vessels_code':vessels_code
            })

    con.commit()
