import fitz  # PyMuPDF

def extract_upper_half(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    new_doc = fitz.open()

    for page in doc:
        rect = page.rect
        upper_half = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 / 2)  # Sélection de la moitié supérieure
        new_page = new_doc.new_page(width=upper_half.width, height=upper_half.height)
        new_page.show_pdf_page(new_page.rect, doc, page.number, clip=upper_half)

    new_doc.save(output_pdf)
    new_doc.close()
    print(f"Nouveau PDF généré : {output_pdf}")

# Exemple d'utilisation
extract_upper_half("input.pdf", "output.pdf")
