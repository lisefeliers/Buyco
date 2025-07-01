from db.database import engine
from models import Base

# Création des tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables créées ")