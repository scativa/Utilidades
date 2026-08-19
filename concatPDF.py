# conda activate hello-test
# pip install pypdf

import os, sys

# Consolas Windows (cp1252) explotan con el emoji del print final
sys.stdout.reconfigure(encoding="utf-8")

from pypdf import PdfReader, PdfWriter


# Ruta de la carpeta con los PDFs
# carpeta_pdf = "."

def concat(carpeta_pdf, out_pdf):
    archivos = sorted([
        f for f in os.listdir(carpeta_pdf) if f.lower().endswith(".pdf")
    ])

    # Crear el escritor para el PDF combinado
    writer = PdfWriter()

    # Agregar cada PDF al escritor
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_pdf, archivo)
        reader = PdfReader(ruta_completa)
        for pagina in reader.pages:
            writer.add_page(pagina)
        print(f"Añadido: {archivo}")

    # Guardar el PDF final
    # salida = os.path.join(carpeta_pdf, "PDF_combinado.pdf")
    with open(out_pdf, "wb") as f:
        writer.write(f)

    print(f"\n✅ PDF combinado creado correctamente: {out_pdf}")

if __name__=="__main__":
    carpeta_pdf = sys.argv[1] if len(sys.argv) > 1 else "."
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else os.path.join("out", "PDF_combinado.pdf")

    # Asegurar que exista la carpeta de salida
    out_dir = os.path.dirname(out_pdf)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    concat(carpeta_pdf, out_pdf)

