import os

folder_path = "pdfs_bis"

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if not filename.lower().endswith(".pdf"):
        continue  # ignorer les fichiers non-PDF

    try:
        with open(file_path, "rb") as f:
            start = f.read(20).lower()
            if start.startswith(b"<html") or b"<html" in start:
                print(f"❌ Faux PDF détecté, suppression : {filename}")
                os.remove(file_path)
            elif not start.startswith(b"%pdf"):
                print(f"⚠️ Format inconnu, suppression par précaution : {filename}")
                os.remove(file_path)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {filename} : {e}")
