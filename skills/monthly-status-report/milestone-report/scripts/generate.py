"""Prepare evidence or render an agent-reviewed milestone report."""
import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from classify import PROJECT_ORDER, prepare_project, validate_plan
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def load_sources(paths):
    if not paths:
        raise ValueError("Supply explicit source snapshots; no unrelated cache or project is selected automatically.")
    projects = []
    for path in paths:
        data = json.loads(Path(path).read_text())
        if not isinstance(data, dict) or not isinstance(data.get("issues"), list):
            raise ValueError(f"Not a JIRA project snapshot: {path}")
        projects.append(data)
    return projects


def set_value(parent, name, **attrs):
    node = OxmlElement(name)
    for key, value in attrs.items():
        node.set(qn("w:" + key), str(value))
    parent.append(node)
    return node


def add_table(doc, headers, rows):
    """Populate the bundled template's plain grid without decorative formatting."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for index, values in enumerate([headers] + rows):
        row = table.rows[0] if index == 0 else table.add_row()
        trpr = row._tr.get_or_add_trPr()
        set_value(trpr, "w:cantSplit")
        if index == 0:
            set_value(trpr, "w:tblHeader")
        for cell, text in zip(row.cells, values):
            cell.text = str(text or "")
            if index == 0:
                for run in cell.paragraphs[0].runs:
                    run.bold = True
    return table


def build_docx(plan, output):
    """Follow assets/milestones_report_template.md without adding design elements."""
    doc = Document()
    doc.core_properties.title = plan["title"]
    doc.core_properties.subject = "INS CPI cBioPortal milestones and deliverables"
    doc.core_properties.author = "Yizhen Chen"

    header = doc.add_paragraph()
    header.add_run(plan["title"]).bold = True
    header.add_run(f"       Version: {plan['version']}")
    doc.add_heading("Schedule Management", level=1)
    doc.add_heading("Milestones", level=2)
    milestones = sorted(plan["milestones"], key=lambda r: (r["delivery_date"], PROJECT_ORDER[r["subproject"]]))
    add_table(doc, ["Subproject", "Milestone", "Delivery Date", "Status"],
              [[r["subproject"], r["milestone"], r["delivery_date"], r["status"]] for r in milestones])
    doc.add_paragraph()
    doc.add_heading("Deliverables", level=2)
    deliverables = sorted(plan["deliverables"], key=lambda r: (PROJECT_ORDER[r["subproject"]], r["date_updated"], r["deliverable_name"]))
    add_table(doc, ["Subproject", "Deliverable Name", "Due Date", "Date Updated", "Status"],
              [[r["subproject"], r["deliverable_name"], r["due_date"], r["date_updated"], r["status"]] for r in deliverables])
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"Choose a new output path to preserve the existing report: {output}")
    doc.save(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--reviewed-json", type=Path)
    parser.add_argument("--period")
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        if not args.period or not args.out:
            parser.error("--prepare requires --period, --source, and --out")
        datetime.strptime(args.period, "%Y-%m")
        projects = load_sources(args.source)
        evidence = {"period": args.period, "sources": [str(Path(p).resolve()) for p in args.source],
                    "projects": [prepare_project(p, args.period) for p in projects]}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2))
        print(f"Evidence prepared for {len(projects)} projects: {args.out}")
        return
    plan = json.loads(args.reviewed_json.read_text())
    projects = load_sources(plan.get("sources", []))
    result = validate_plan(plan, projects)
    print(json.dumps(result))
    if args.validate_only:
        return
    timestamp = datetime.now(ZoneInfo("America/New_York")).strftime("%Y%m%d_%H%M%S")
    output = args.out or Path(f"Milestone_Report_{plan['period'].replace('-', '')}_revised_{timestamp}.docx")
    print(f"Saved: {build_docx(plan, output)}")


if __name__ == "__main__":
    main()
