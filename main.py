import fitz  # PyMuPDF

def extract_upper_half_with_links(input_pdf, output_pdf):
    try:
        # Ouvrir le PDF d'entrée
        doc = fitz.open(input_pdf)
    except Exception as e:
        print(f"Erreur lors de l'ouverture du PDF : {e}")
        return

    # Créer un nouveau PDF pour la sortie
    new_doc = fitz.open()

    # Parcourir chaque page du PDF
    for page_num, page in enumerate(doc, start=1):
        try:
            rect = page.rect
            upper_half = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 / 2)  # Sélectionner la moitié supérieure
            new_page = new_doc.new_page(width=upper_half.width, height=upper_half.height)
            new_page.show_pdf_page(new_page.rect, doc, page.number, clip=upper_half)

            print(f"Page {page_num}: Moitié supérieure copiée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'extraction de la moitié supérieure de la page {page_num}: {e}")
            continue  # Continuer avec les autres pages même si celle-ci échoue

        # Copier les liens de la page
        for link_num, link in enumerate(page.get_links(), start=1):
            print(f"Page {page_num}, Lien {link_num}: Traitement du lien.")

            # Étape 1: Vérifier si la clé 'from' est présente
            if "from" not in link:
                print(f"Page {page_num}, Lien {link_num}: La clé 'from' est absente dans ce lien.")
                continue  # Passer au lien suivant

            # Étape 2: Extraire les coordonnées du lien
            try:
                link_rect = fitz.Rect(link["from"])
                print(f"Page {page_num}, Lien {link_num}: Coordonnées du lien extraites: {link_rect}")
            except Exception as e:
                print(f"Page {page_num}, Lien {link_num}: Erreur lors de l'extraction des coordonnées du lien: {e}")
                continue  # Passer au lien suivant

            # Étape 3: Vérifier si le lien est dans la moitié supérieure
            try:
                if link_rect.y1 > upper_half.y1:
                    print(f"Page {page_num}, Lien {link_num}: Le lien est en dehors de la moitié supérieure de la page.")
                    continue  # Passer au lien suivant si le lien n'est pas dans la moitié supérieure
            except Exception as e:
                print(f"Page {page_num}, Lien {link_num}: Erreur lors de la vérification de la position du lien: {e}")
                continue  # Passer au lien suivant

            # Étape 4: Insérer le lien dans la nouvelle page
            try:
                new_page.insert_link({
                    'from': link_rect,  # Utiliser les coordonnées du lien
                    'uri': link.get("uri"),  # URI du lien
                    'kind': link.get("kind", fitz.LINK_URI),  # Type de lien (par défaut URI si non spécifié)
                    'page': link.get("page")  # Pour les liens internes (optionnel)
                })

                print(f"Page {page_num}, Lien {link_num}: Lien inséré avec succès.")
            except Exception as e:
                print(f"Page {page_num}, Lien {link_num}: Erreur lors de l'insertion du lien: {e}")
                continue  # Passer au lien suivant

    # Sauvegarder le nouveau PDF avec les liens
    try:
        new_doc.save(output_pdf)
        new_doc.close()
        print(f"Nouveau PDF généré avec succès : {output_pdf}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du PDF généré : {e}")

# Exemple d'utilisation
extract_upper_half_with_links("input.pdf", "output.pdf")



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_pdf> <output_pdf>")
    else:
        extract_upper_half_with_links(sys.argv[1], sys.argv[2])