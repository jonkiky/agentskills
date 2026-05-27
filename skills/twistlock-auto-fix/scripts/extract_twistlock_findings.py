#!/usr/bin/env python3
"""Extract Critical/High CVE-like findings from Twistlock JSON artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CVE_RE = re.compile(r"(CVE-\d{4}-\d+)", re.IGNORECASE)
TARGET_SEVERITIES = {"critical", "high"}


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk(item)


def first_value(data: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = data.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def parse_finding(data: dict, source: str) -> dict | None:
    cve = ""
    for key in ("cve", "cveId", "cveID", "id", "name"):
        value = data.get(key)
        if isinstance(value, str):
            match = CVE_RE.search(value)
            if match:
                cve = match.group(1).upper()
                break
    if not cve:
        return None

    severity = first_value(data, ("severity", "risk", "cvssSeverity", "impact")).lower()
    if severity not in TARGET_SEVERITIES:
        return None

    package = first_value(data, ("packageName", "package", "fullPackageName", "pkgName", "name"))
    installed = first_value(data, ("packageVersion", "version", "installedVersion", "currentVersion"))
    fixed = first_value(data, ("fixedVersion", "fixVersion", "patchedVersion", "upgradeVersion"))
    title = first_value(data, ("title", "description", "text"))

    return {
        "source": source,
        "cve": cve,
        "severity": severity.capitalize(),
        "package": package,
        "installed_version": installed,
        "fixed_version": fixed,
        "title": title,
    }


def read_findings(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    dedup = {}
    for node in walk(payload):
        finding = parse_finding(node, str(path))
        if finding:
            key = (
                finding["source"],
                finding["cve"],
                finding["package"],
                finding["installed_version"],
            )
            dedup[key] = finding
    return sorted(
        dedup.values(),
        key=lambda f: (0 if f["severity"].lower() == "critical" else 1, f["cve"], f["package"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Twistlock detailed.json files or artifact directories")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = parser.parse_args()

    files: list[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.glob("*/detailed.json")))
            if (path / "detailed.json").exists():
                files.append(path / "detailed.json")
        else:
            files.append(path)

    findings: list[dict] = []
    for file_path in files:
        findings.extend(read_findings(file_path))

    if args.json:
        print(json.dumps(findings, indent=2, sort_keys=True))
        return 0 if not findings else 1

    headers = ("Severity", "CVE", "Package", "Installed", "Fixed", "Source")
    widths = (9, 18, 26, 16, 16, 42)
    print(" | ".join(h.ljust(w) for h, w in zip(headers, widths)))
    print("-" * 138)
    for finding in findings:
        row = (
            finding["severity"],
            finding["cve"],
            finding["package"] or "-",
            finding["installed_version"] or "-",
            finding["fixed_version"] or "-",
            finding["source"],
        )
        print(" | ".join(str(value)[:width].ljust(width) for value, width in zip(row, widths)))

    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
