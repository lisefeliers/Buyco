from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Data(Base):
    __tablename__ = 'Maritimes'
    id_carrier = Column(Integer, primary_key=True)
    name_route = Column(String)
    code_route = Column(Integer)
    port_name = Column(String)
    port_code = Column(Integer)
    terminal = Column(String)
    vessels = Column(String)


    """user = User(name="Alice", age=25)
session.add(user) On doit modifier et automatiser pour les ajouter dans le doc
session.commit()"""