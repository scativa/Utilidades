"""Rotate every page of a PDF by 180 degrees.

Usage:
    python rotate_pdf.py <input.pdf> [output.pdf]

If output.pdf is omitted, the output is written to out/<stem>_rotated.pdf
(the out/ folder is created if missing). The input file is never modified.
"""

import sys
from pathlib import Path

import pymupdf  # PyMuPDF (available in the pdf_env conda environment)


def rotate_pdf(input_path: Path, output_path: Path) -> int:
    """Rotate all pages 180 degrees and save to output_path.

    Returns the number of pages processed.
    """
    doc = pymupdf.open(input_path)
    try:
        page_count = doc.page_count
        for page in doc:
            # Keep rotation additive: 0 <-> 180, 90 <-> 270
            page.set_rotation((page.rotation + 180) % 360)
        # garbage=3 compacts; garbage=4 would close the doc during save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path, garbage=3, deflate=True)
    finally:
        doc.close()
    return page_count


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(
            "Usage: python rotate_pdf.py <input.pdf> [output.pdf]",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[1])
    if not input_path.is_file():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1
    if input_path.suffix.lower() != ".pdf":
        print(f"Error: not a PDF file: {input_path}", file=sys.stderr)
        return 1

    output_path = (
        Path(argv[2])
        if len(argv) == 3
        else Path("out") / f"{input_path.stem}_rotated.pdf"
    )
    if output_path == input_path:
        print("Error: output path must differ from input path", file=sys.stderr)
        return 1

    try:
        page_count = rotate_pdf(input_path, output_path)
    except Exception as exc:
        print(f"Error: failed to rotate PDF: {exc}", file=sys.stderr)
        return 1

    print(f"Rotated {page_count} page(s) -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
