import argparse
import os
import fitz  # PyMuPDF

def replace_text_in_pdf(input_pdf, output_pdf, search_text, replace_text):
    """
    Reemplaza texto en un PDF.
    Concepto clave: Un PDF no es un documento de texto, es un lienzo de dibujo.
    Esta función "borra" visualmente el texto viejo (redaction) y escribe el nuevo encima.
    """
    try:
        doc = fitz.open(input_pdf)
    except Exception as e:
        print(f"Error al abrir el PDF: {e}")
        return

    replacements_made = 0

    for page in doc:
        # Buscamos las coordenadas (bounding boxes) donde está el texto
        text_instances = page.search_for(search_text)
        
        for inst in text_instances:
            # 1. Borrar (Redactar) el texto original
            # Ocultamos el texto original (por defecto con blanco). 
            # Si tu PDF tiene fondo de color, habría que ajustar el 'fill'.
            page.add_redact_annot(inst, fill=(1, 1, 1))
            page.apply_redactions()
            
            # 2. Escribir el nuevo texto
            # Calculamos una posición aproximada y un tamaño de fuente 
            # basado en el alto de la caja del texto original.
            font_size = inst.y1 - inst.y0
            # Ajustamos levemente la posición vertical para la línea base de la fuente
            point = fitz.Point(inst.x0, inst.y1 - (font_size * 0.2)) 
            
            page.insert_text(point, replace_text, fontsize=font_size, color=(0, 0, 0))
            replacements_made += 1

    if replacements_made > 0:
        try:
            doc.save(output_pdf)
            print(f"¡Éxito! Se realizaron {replacements_made} reemplazos. Archivo guardado en: {output_pdf}")
        except Exception as e:
            print(f"Error al guardar el PDF: {e}")
    else:
        print("No se encontró el texto buscado en el PDF. No se generó archivo de salida.")

def main():
    parser = argparse.ArgumentParser(
        description="Reemplaza un texto específico en un archivo PDF."
    )
    parser.add_argument("input_pdf", help="Ruta al archivo PDF original")
    parser.add_argument("search_text", help="Texto que querés buscar y reemplazar")
    parser.add_argument("replace_text", help="El nuevo texto que querés insertar")
    parser.add_argument(
        "output_pdf",
        nargs="?",
        default=None,
        help="Ruta donde se guardará el nuevo PDF (default: out/<input>_reemplazado.pdf)",
    )

    args = parser.parse_args()

    output_pdf = args.output_pdf
    if output_pdf is None:
        base = os.path.splitext(os.path.basename(args.input_pdf))[0]
        output_pdf = os.path.join("out", f"{base}_reemplazado.pdf")

    # Asegurar que exista la carpeta de salida
    out_dir = os.path.dirname(output_pdf)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    replace_text_in_pdf(args.input_pdf, output_pdf, args.search_text, args.replace_text)

if __name__ == "__main__":
    main()
