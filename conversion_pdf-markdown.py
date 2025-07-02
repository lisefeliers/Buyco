from markitdown import MarkItDown



# Conversion pdf en Markdown

markitdown = MarkItDown()
result = markitdown.convert("pdfs/WAX_0.pdf")
output_file = "WAX_0.md"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(result.text_content)


