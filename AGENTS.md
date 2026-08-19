# AGENTS.md

Standalone one-off utility scripts for PDF/H5P processing on Windows. Not a package, not a git repo — there is no VCS safety net, so keep backups before destructive edits.

## Conda environments (critical)

Scripts require specific conda envs; the active `base` env has **no** PDF libraries. Activate the env first, or call the env's python explicitly.

| Script | Env | Library |
|---|---|---|
| `rotate_pdf.py`, `pdf_replace.py`, `h5p_a_pdf.py` | `pdf_env` | PyMuPDF 1.28.0 (both `import pymupdf` and `import fitz` work) + reportlab |
| `concatPDF.py` | `hello-test` | pypdf 5.4.0 |
| `convertir_h5P_all.ps1` | env active when launched | runs `python h5p_a_pdf.py` → needs `pdf_env` active |

```powershell
conda activate pdf_env
python rotate_pdf.py "archivo.pdf"
```

## Script usage

- `rotate_pdf.py <in.pdf> [out.pdf]` — rotates every page 180°; default output `out/<stem>_rotated.pdf`; input untouched.
- `pdf_replace.py <in.pdf> <search> <replace> [out.pdf]` — visually redacts the old text and writes the new text over it (PDF is a drawing canvas, not text); output defaults to `out/<stem>_reemplazado.pdf`.
- `h5p_a_pdf.py <file.h5p>` — H5P is a ZIP: extracts to `temp_<base>/`, reads `content/content.json` for text/images, builds the PDF with reportlab into `out/<base>.pdf`, then deletes the temp dir.
- `concatPDF.py [folder] [out.pdf]` — concatenates every PDF in `folder` (default `.` → `out/PDF_combinado.pdf`).
- `convertir_h5P_all.ps1` — batch-converts every `.h5p` in the current folder.

## Repo quirks

- Paths with spaces are common (`Servicios TIC/`, `Compra Venta Bilbao 1405.pdf`): always quote arguments in PowerShell.
- `temp_h5p/` and `temp_/` at the root are leftovers from interrupted `h5p_a_pdf.py` runs, not source.
- PyMuPDF trap: `doc.save(..., garbage=4)` closes the document during save — read `doc.page_count` before saving (comment in `rotate_pdf.py`).
- User-facing script output mixes Spanish (`concatPDF.py`, `h5p_a_pdf.py`, `pdf_replace.py`, `convertir_h5P_all.ps1`) and English (`rotate_pdf.py`); match the file you edit, don't unify.