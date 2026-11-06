"""Evidence selection and validation; the agent writes semantic summaries."""

import re
from datetime import date

PROJECT_ALIASES = {
    "ins": "INS", "index of nci studies": "INS",
    "cpi": "CPI", "ccdi cpi": "CPI",
    "cbio": "cBioPortal", "cbioportal": "cBioPortal", "ccdi cbioportal": "cBioPortal",
}
PROJECT_ORDER = {"INS": 0, "CPI": 1, "cBioPortal": 2}
ELIGIBLE_STATES = {"closed", "done", "resolved", "completed", "testing", "ready for qa testing", "ready for review"}
BAD_RESOLUTIONS = {"cancelled", "canceled", "duplicate", "won't fix", "wont fix", "won’t fix", "not a bug", "incomplete"}
MILESTONE_KINDS = {"product_release", "stage_promotion", "major_capability", "major_migration"}
QUALIFICATIONS = {"implemented", "dev_validated", "qa_testing", "completed_output"}
TICKET_RE = re.compile(r"\b[A-Z][A-Z0-9_]*-\d+\b")


def canonical_project(name):
    label = PROJECT_ALIASES.get(str(name).strip().casefold())
    if not label:
        raise ValueError(f"Unsupported project: {name}. Use INS, CPI, or cBioPortal.")
    return label


def normalized_date(value):
    if not value:
        return ""
    value = str(value)[:10]
    date.fromisoformat(value)
    return value


def due_date(issue):
    return normalized_date(issue.get("duedate")) or normalized_date(issue.get("completed_sprint_date"))


def candidate_exclusion(issue, period):
    state = str(issue.get("status", "")).strip().casefold()
    resolution = str(issue.get("resolution", "")).strip().casefold()
    if resolution in BAD_RESOLUTIONS:
        return f"Non-delivery resolution: {resolution}"
    if state not in ELIGIBLE_STATES:
        return f"Implementation/delivery not established by workflow: {state}"
    resolved = normalized_date(issue.get("resolution_date"))
    if resolved and resolved[:7] != period:
        return f"Historical completion recorded {resolved}"
    comments = sorted(issue.get("comments") or [], key=lambda c: c.get("date", ""))
    last = comments[-1].get("body", "").casefold() if comments else ""
    if re.search(r"decided not to (?:move forward|proceed)|decide(?:d)? not to change anything|wrong ticket type|ticket created by mistake", last):
        return "Closed without an implemented change"
    return ""


def prepare_project(project, period):
    label = canonical_project(project.get("project_name") or project["display_name"])
    return {
        **project,
        "subproject": label,
        "review": [
            {"source_key": i["issue_key"], "exclusion": candidate_exclusion(i, period),
             "review_required": "Verify delivery, significance, duplicate outcomes, and summary wording."}
            for i in project.get("issues", [])
        ],
    }


def validate_plan(plan, projects):
    """Reject mechanically misleading output; evidence meaning needs agent review."""
    period = plan.get("period", "")
    if not re.fullmatch(r"\d{4}-\d{2}", period):
        raise ValueError("period must be YYYY-MM")
    date.fromisoformat(period + "-01")
    cutoff = normalized_date(plan.get("as_of"))
    if not cutoff or cutoff[:7] != period:
        raise ValueError("as_of must be within the reporting period")
    for field in ("title", "version"):
        if not str(plan.get(field, "")).strip():
            raise ValueError(f"Missing {field}")
    index, labels = {}, set()
    for project in projects:
        label = canonical_project(project.get("project_name") or project["display_name"])
        if label in labels:
            raise ValueError(f"Duplicate source project: {label}")
        labels.add(label)
        source_period = project.get("reporting_period", {})
        if source_period and (source_period.get("start") != period + "-01" or source_period.get("end_inclusive") != cutoff):
            raise ValueError(f"Source reporting period does not match plan: {label}")
        for issue in project.get("issues", []):
            key = issue["issue_key"]
            if key in index:
                raise ValueError(f"Duplicate source key: {key}")
            index[key] = (label, issue)
    used_keys, used_names = set(), set()
    for table, name_field in (("milestones", "milestone"), ("deliverables", "deliverable_name")):
        if not isinstance(plan.get(table), list):
            raise ValueError(f"{table} must be a list")
        for row in plan[table]:
            label = row.get("subproject")
            if label not in PROJECT_ORDER or label not in labels:
                raise ValueError(f"Noncanonical or unsourced Subproject: {label}")
            name = str(row.get(name_field, "")).strip()
            status = str(row.get("status", "")).strip()
            if not name or TICKET_RE.search(name):
                raise ValueError(f"Missing name or ticket number in displayed name: {name}")
            if not 1 <= len(status.split()) <= 24:
                raise ValueError(f"Status must contain 1–24 words: {name}")
            if "…" in status or "..." in status or "\n" in status or TICKET_RE.search(status) or re.search(r"https?://", status):
                raise ValueError(f"Rewrite status without truncation, links, or ticket IDs: {name}")
            identity = (label, re.sub(r"\W+", " ", name).strip().casefold())
            if identity in used_names:
                raise ValueError(f"Duplicate outcome name: {name}")
            used_names.add(identity)
            keys = row.get("source_keys", [])
            if not keys or len(keys) != len(set(keys)):
                raise ValueError(f"Missing or duplicate source keys: {name}")
            issues = []
            for key in keys:
                if key not in index or index[key][0] != label:
                    raise ValueError(f"Missing or cross-project source: {key}")
                if key in used_keys:
                    raise ValueError(f"Repeated source outcome; consolidate rows: {key}")
                issue = index[key][1]
                reason = candidate_exclusion(issue, period)
                if reason:
                    raise ValueError(f"Ineligible source {key}: {reason}")
                if normalized_date(issue.get("updated")) > cutoff:
                    raise ValueError(f"Source is newer than snapshot: {key}")
                issues.append(issue)
                used_keys.add(key)
            if not str(row.get("evidence", "")).strip():
                raise ValueError(f"Missing evidence review: {name}")
            if table == "milestones":
                delivery = normalized_date(row.get("delivery_date"))
                if not delivery or delivery[:7] != period or delivery > cutoff:
                    raise ValueError(f"Milestone needs an in-period achieved date: {name}")
                if row.get("kind") not in MILESTONE_KINDS or not row.get("significance") or not row.get("date_basis"):
                    raise ValueError(f"Missing major-event justification/date basis: {name}")
            else:
                if row.get("qualification") not in QUALIFICATIONS:
                    raise ValueError(f"Missing implementation/validation qualification: {name}")
                updated = max(normalized_date(i.get("updated")) for i in issues)
                if normalized_date(row.get("date_updated")) != updated:
                    raise ValueError(f"Date Updated must match latest source update ({updated}): {name}")
                due = normalized_date(row.get("due_date"))
                supported = {due_date(i) for i in issues if due_date(i)}
                if due and supported != {due}:
                    raise ValueError(f"Due Date must be a supported common target or blank: {name}")
    for entry in plan.get("exclusions", []):
        if entry.get("source_key") not in index or not entry.get("reason"):
            raise ValueError("Exclusions require a known source key and a reason")
        if entry["source_key"] in used_keys:
            raise ValueError(f"Source both included and excluded: {entry['source_key']}")
    return {"projects": sorted(labels, key=PROJECT_ORDER.get), "milestones": len(plan["milestones"]),
            "deliverables": len(plan["deliverables"]), "max_status_words": max(
                [len(r["status"].split()) for t in ("milestones", "deliverables") for r in plan[t]] or [0])}
