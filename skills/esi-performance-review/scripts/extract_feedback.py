#!/usr/bin/env python3
"""Extract candidate employee feedback from top-level DOCX files, read-only."""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": W[1:-1]}
EXCLUDED = {W + "del", W + "moveFrom"}


def normalize(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def paragraph_text(paragraph):
    def visit(node):
        if node.tag in EXCLUDED or (node is not paragraph and node.tag == W + "p"):
            return ""
        if node.tag == W + "t":
            return node.text or ""
        if node.tag == W + "tab":
            return "\t"
        if node.tag in {W + "br", W + "cr"}:
            return "\n"
        return "".join(visit(child) for child in node)

    return visit(paragraph).strip()


def extract_paragraphs(root):
    parents = {child: parent for parent in root.iter() for child in parent}
    paragraphs = []
    for index, paragraph in enumerate(root.iter(W + "p"), 1):
        ancestor = parents.get(paragraph)
        excluded = False
        while ancestor is not None:
            if ancestor.tag in EXCLUDED:
                excluded = True
                break
            ancestor = parents.get(ancestor)
        if excluded:
            continue
        text = paragraph_text(paragraph)
        if text:
            record = {"id": f"P{index:03d}", "text": text}
            style = paragraph.find("w:pPr/w:pStyle", NS)
            if style is not None:
                record["style"] = style.get(W + "val")
            paragraphs.append(record)
    return paragraphs


def read_docx(path):
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        paragraphs = extract_paragraphs(root)
        warnings = []
        for tag, label in [
            ("ins", "tracked insertions"),
            ("del", "tracked deletions"),
            ("moveFrom", "tracked moves from"),
            ("moveTo", "tracked moves to"),
            ("drawing", "drawings or embedded images"),
            ("pict", "legacy pictures or text boxes"),
            ("altChunk", "externally embedded content"),
        ]:
            count = len(list(root.iter(W + tag)))
            if count:
                warnings.append(f"Contains {count} {label}; inspect relevant original content.")

        comments = []
        if "word/comments.xml" in archive.namelist():
            comment_root = ET.fromstring(archive.read("word/comments.xml"))
            for comment in comment_root.iter(W + "comment"):
                comments.append({
                    "id": comment.get(W + "id"),
                    "author": comment.get(W + "author"),
                    "date": comment.get(W + "date"),
                    "text": "\n".join(p["text"] for p in extract_paragraphs(comment)),
                })
            if comments:
                warnings.append("Comments are separate review annotations, not automatically final feedback.")

        for part in ("word/footnotes.xml", "word/endnotes.xml"):
            if part in archive.namelist():
                note_root = ET.fromstring(archive.read(part))
                if extract_paragraphs(note_root):
                    warnings.append(f"Additional text exists in {part}; inspect the original notes.")

        body_text = "\n".join(p["text"] for p in paragraphs)
        return {
            "path": str(path.resolve()),
            "paragraphs": paragraphs,
            "comments": comments,
            "warnings": warnings,
            "text_sha256": hashlib.sha256(body_text.encode("utf-8")).hexdigest(),
        }


def extract_folder(folder, employee, aliases):
    terms = list(dict.fromkeys(normalize(s) for s in [employee, *aliases] if normalize(s)))
    patterns = [re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)") for term in terms]
    paths = sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".docx" and not p.name.startswith("~$")),
        key=lambda p: p.name.casefold(),
    )
    candidates, unmatched, errors, fingerprints = [], [], [], {}
    for path in paths:
        try:
            document = read_docx(path)
        except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError, RuntimeError) as exc:
            errors.append({"path": str(path.resolve()), "error": str(exc)})
            continue
        matches = [
            p["id"] for p in document["paragraphs"]
            if any(pattern.search(normalize(p["text"])) for pattern in patterns)
        ]
        filename_hint = any(pattern.search(normalize(path.stem.replace("_", " "))) for pattern in patterns)
        if not matches and not filename_hint:
            unmatched.append(path.name)
            continue
        document["matching_paragraphs"] = matches
        document["candidate_basis"] = "body_name_match" if matches else "filename_only"
        if not matches:
            document["warnings"].append("Filename matches but body does not; employee identity is unconfirmed.")
        fingerprint = document["text_sha256"]
        if fingerprint in fingerprints:
            document["same_body_text_as"] = fingerprints[fingerprint]
        else:
            fingerprints[fingerprint] = str(path.resolve())
        candidates.append(document)
    return {
        "employee": employee,
        "search_terms": terms,
        "folder": str(folder.resolve()),
        "scanned_docx_count": len(paths),
        "candidate_note": "A name match is a candidate, not proof of the review subject. Confirm context before use.",
        "candidates": candidates,
        "unmatched_files": unmatched,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--employee", required=True)
    parser.add_argument("--alias", action="append", default=[])
    parser.add_argument("--output", type=Path, help="Write JSON here; default is stdout.")
    args = parser.parse_args()
    if not args.folder.is_dir():
        parser.error("--folder must be an existing directory")
    if not normalize(args.employee):
        parser.error("--employee must not be empty")
    if any(not normalize(alias) for alias in args.alias):
        parser.error("--alias must not be empty")
    if args.output and args.output.suffix.lower() != ".json":
        parser.error("--output must end in .json to avoid overwriting a source document")
    result = extract_folder(args.folder, args.employee, args.alias)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(f"Scanned {result['scanned_docx_count']} DOCX files; found {len(result['candidates'])} candidates; {len(result['errors'])} errors. Evidence: {args.output}")
    else:
        sys.stdout.write(payload)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
