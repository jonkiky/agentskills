#!/usr/bin/env python3
"""Extract report evidence from DOCX/PDF files without changing the sources."""

import argparse
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
SKIP = {W + "del", W + "moveFrom", W + "instrText"}


def visible_text(element):
    """Keep displayed text, including insertions, but omit deleted text/fields."""
    if element.tag in SKIP:
        return ""
    if element.tag == W + "t":
        return element.text or ""
    if element.tag == W + "tab":
        return "\t"
    if element.tag in {W + "br", W + "cr"}:
        return "\n"
    return "".join(visible_text(child) for child in element)


def docx_paragraphs(element, location):
    """Walk paragraphs in source order, retaining table/cell paths as locators."""
    counts = {}
    for child in element:
        if child.tag in SKIP:
            continue
        tag = child.tag.rsplit("}", 1)[-1]
        counts[tag] = counts.get(tag, 0) + 1
        child_location = f"{location}/{tag}[{counts[tag]}]"
        if child.tag == W + "p":
            text = visible_text(child).strip()
            if text:
                yield {"location": child_location, "text": text}
        else:
            yield from docx_paragraphs(child, child_location)


def extract_docx(path):
    blocks, warnings = [], []
    with ZipFile(path) as archive:
        parts = ["word/document.xml"]
        parts.extend(sorted(
            name for name in archive.namelist()
            if name.startswith(("word/header", "word/footer"))
            and name.endswith(".xml")
        ))
        parts.extend(
            name for name in ("word/footnotes.xml", "word/endnotes.xml")
            if name in archive.namelist()
        )
        for part in parts:
            root = ET.fromstring(archive.read(part))
            if part == "word/document.xml" and root.find(W + "body") is None:
                raise ValueError("Unsupported Word XML; convert to a standard DOCX or PDF.")
            tags = {element.tag for element in root.iter()}
            if tags & {W + "ins", W + "del", W + "moveFrom", W + "moveTo"}:
                warnings.append(
                    f"{part}: tracked changes present; extracted text includes insertions "
                    "and excludes deletions. Review the intended version."
                )
            if tags & {W + "drawing", W + "pict", W + "object", W + "altChunk"}:
                warnings.append(
                    f"{part}: visual or embedded content present; inspect for report "
                    "information that text extraction may miss."
                )
            blocks.extend(docx_paragraphs(root, part))
    if not blocks:
        warnings.append("No extractable Word text; inspect visually before classifying.")
    return blocks, warnings


def extract_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF extraction requires pypdf; use the bundled runtime.") from exc

    reader = PdfReader(path)
    if reader.is_encrypted and not reader.decrypt(""):
        raise ValueError("Password-protected PDF; a readable copy is needed.")
    blocks, warnings = [], []
    for number, page in enumerate(reader.pages, 1):
        contents = page.get_contents()
        text = (page.extract_text(extraction_mode="layout") or "").strip() if contents is not None else ""
        blocks.append({"location": f"page {number}", "page": number, "text": text})
        if len("".join(text.split())) < 50:
            warnings.append(
                f"Page {number}: sparse or missing text; visually inspect and use OCR "
                "if needed before concluding there is no AI content."
            )
        if contents is not None and len(page.images):
            warnings.append(
                f"Page {number}: images present; inspect for information that the "
                "text layer may omit."
            )
    if not blocks:
        warnings.append("PDF has no pages; no report content was extracted.")
    return blocks, warnings


def extract_one(path):
    source = path.expanduser().resolve()
    result = {"source": str(source), "format": source.suffix.lower().lstrip(".")}
    try:
        if not source.is_file():
            raise FileNotFoundError("Input file does not exist or is not a regular file.")
        if source.suffix.lower() == ".docx":
            blocks, warnings = extract_docx(source)
        elif source.suffix.lower() == ".pdf":
            blocks, warnings = extract_pdf(source)
        elif source.suffix.lower() == ".doc":
            raise ValueError("Legacy DOC: convert a temporary copy to DOCX or PDF first.")
        else:
            raise ValueError("Unsupported report format; provide DOCX or PDF.")
        result.update(status="needs_review" if warnings else "ok",
                      blocks=blocks, warnings=warnings)
    except Exception as exc:
        result.update(status="error", blocks=[], warnings=[],
                      error=f"{type(exc).__name__}: {exc}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path, help="Explicit DOCX or PDF files")
    parser.add_argument("--output", type=Path, help="New JSON file; defaults to stdout")
    args = parser.parse_args()
    if args.output:
        args.output = args.output.expanduser().resolve()
        if args.output.exists():
            parser.error("Output already exists; choose a new temporary output path.")
        if args.output in {path.expanduser().resolve() for path in args.reports}:
            parser.error("Output must not replace an input report.")

    documents = [extract_one(path) for path in args.reports]
    content = json.dumps({"schema_version": 1, "documents": documents},
                         ensure_ascii=False, indent=2) + "\n"
    if args.output:
        try:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(content)
        except OSError as exc:
            parser.error(str(exc))
        print(f"Extracted {len(documents)} report(s) to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(content)
    if any(document["status"] == "error" for document in documents):
        return 1
    if any(document["status"] == "needs_review" for document in documents):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
