# Utilidades — PDF & H5P Processing Utilities

Standalone one-off scripts for PDF and H5P file processing on Windows (PowerShell).

## Prerequisites

Each script needs its own conda environment. The `base` environment has **no** PDF libraries, so activate the right environment first:

| Script | Environment | Library |
|---|---|---|
| `rotate_pdf.py`, `pdf_replace.py`, `h5p_a_pdf.py` | `pdf_env` | PyMuPDF 1.28.0 + reportlab |
| `concatPDF.py` | `hello-test` | pypdf 5.4.0 |
| `convertir_h5P_all.ps1` | active env must be `pdf_env` | runs `h5p_a_pdf.py` |

```powershell
conda activate pdf_env
```

## Scripts

### rotate_pdf.py — Rotate every page 180°

Rotates all pages of a PDF by 180 degrees. The input file is never modified; the output is written to a new file.

```
python rotate_pdf.py <input.pdf> [output.pdf]
```

Examples:

```powershell
python rotate_pdf.py "Compra Venta Bilbao 1405.pdf"
# creates: out/Compra Venta Bilbao 1405_rotated.pdf

python rotate_pdf.py "Compra Venta Bilbao 1405.pdf" "Rotar\salida.pdf"
```

### pdf_replace.py — Replace text in a PDF

Finds the given text on every page and replaces it visually: it redacts (hides) the old text with a white box and writes the new text over it. A PDF is a drawing canvas, not a text document, so the replacement is visual — it does not change the underlying text layer.

```
python pdf_replace.py <input.pdf> <search_text> <replace_text> [output.pdf]
```

Example:

```powershell
python pdf_replace.py "contrato.pdf" "ACTA 2020" "ACTA 2024"
# creates: out/contrato_reemplazado.pdf
```

If omitted, the output defaults to `out/<input>_reemplazado.pdf`.

If the search text is not found, no output file is created.

### h5p_a_pdf.py — Convert an H5P course to PDF

H5P packages are ZIP archives. This script extracts the package, walks `content/content.json` looking for text blocks and images, and builds a letter-size PDF with reportlab. Temporary files are removed automatically.

```
python h5p_a_pdf.py <file.h5p>
```

Example:

```powershell
python h5p_a_pdf.py "1 (3).h5p"
# creates: out/1 (3).pdf
```

### concatPDF.py — Merge all PDFs in a folder

Concatenates every `.pdf` in a folder (sorted alphabetically) into a single file.

```
python concatPDF.py [folder] [output.pdf]
```

Examples:

```powershell
python concatPDF.py
# merges every PDF in the current folder into out/PDF_combinado.pdf

python concatPDF.py "Servicios TIC" "Manual completo.pdf"
```

### convertir_h5P_all.ps1 — Batch convert H5P files

PowerShell wrapper that runs `h5p_a_pdf.py` for every `.h5p` file in the current folder. Useful when you have many courses to convert at once.

```powershell
conda activate pdf_env
.\convertir_h5P_all.ps1
```

## Notes

- Paths with spaces are common (`Servicios TIC`, `1 (1).h5p`): always wrap arguments in double quotes.
- Generated files default to the `out/` folder (created automatically if missing); explicit output paths still work.
- A failed or interrupted `h5p_a_pdf.py` run can leave a `temp_*` folder behind; these are byproducts and safe to delete.