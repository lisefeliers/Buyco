from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine, text

metadata = MetaData()
data_table = Table('data', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_carrier', String(50)),
    Column('code_route', String(50)),
    Column('name_route', String(100)),
    Column('port_code', String(50)),
    Column('port_name', String(100)),
    Column('terminal', String(100)),
    Column('vessels', String(100)),
)

# Connexion et création
engine = create_engine('mysql+pymysql://root:rootinfo8988*Mines@localhost:3306/app', echo=True)
metadata.create_all(engine)