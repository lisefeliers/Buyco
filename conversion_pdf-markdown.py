from markitdown import MarkItDown
import pdfplumber



# Conversion pdf en Markdown

markitdown = MarkItDown()
result = markitdown.convert("test.pdf") #pdfs/WAX_0.pdf
output_file = "test.md" #"WAX_0.md"

#with open(output_file, "w", encoding="utf-8") as file:
#    file.write(result.text_content)



# Autre script pour convertir pdf en Markdown

def pdf_tables_to_markdown(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for i, table in enumerate(tables, 1):
                # Construire la table Markdown
                md = ""
                # Entête
                md += "| " + " | ".join(table[0]) + " |\n"
                md += "| " + " | ".join(["---"]*len(table[0])) + " |\n"
                # Lignes
                for row in table[1:]:
                    md += "| " + " | ".join(cell if cell else "" for cell in row) + " |\n"

                # Sauvegarder chaque tableau en markdown
                with open(f"test.md", "w", encoding="utf-8") as f:
                    f.write(md)

pdf_tables_to_markdown("test.pdf")
