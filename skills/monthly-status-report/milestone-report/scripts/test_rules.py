"""Regression checks for misleading report output."""
import copy
import unittest
from classify import canonical_project, candidate_exclusion, due_date, validate_plan

class ReportRules(unittest.TestCase):
    def fixture(self):
        issue = {"issue_key": "INS-1", "summary": "Implemented feature", "status": "Testing",
                 "updated": "2026-10-23", "resolution": "", "resolution_date": "",
                 "duedate": "", "completed_sprint_date": "", "comments": []}
        project = {"project_name": "INS", "issues": [issue],
                   "reporting_period": {"start": "2026-10-01", "end_inclusive": "2026-10-28"}}
        row = {"subproject": "INS", "deliverable_name": "Implemented feature",
               "status": "Implemented and validated on development; QA testing is underway.",
               "source_keys": ["INS-1"], "evidence": "Development validation confirmed.",
               "qualification": "qa_testing", "date_updated": "2026-10-23", "due_date": ""}
        plan = {"title": "October report", "version": "Revised", "period": "2026-10",
                "as_of": "2026-10-28", "milestones": [], "deliverables": [row]}
        return plan, [project]

    def test_scope_and_aliases(self):
        self.assertEqual(canonical_project("Index of NCI Studies"), "INS")
        self.assertEqual(canonical_project("CCDI CPI"), "CPI")
        self.assertEqual(canonical_project("CBIO"), "cBioPortal")
        with self.assertRaises(ValueError):
            canonical_project("FEDERATION")

    def test_done_does_not_override_cancellation_or_no_change(self):
        issue = {"status": "Closed", "resolution": "Cancelled"}
        self.assertTrue(candidate_exclusion(issue, "2026-10"))
        issue.update(resolution="Done", comments=[{"date": "2026-10-28", "body": "Decided not to move forward with the feature."}])
        self.assertTrue(candidate_exclusion(issue, "2026-10"))

    def test_historical_and_unfinished_work_excluded(self):
        self.assertTrue(candidate_exclusion({"status": "On Hold"}, "2026-10"))
        self.assertTrue(candidate_exclusion({"status": "Closed", "resolution_date": "2026-09-15"}, "2026-10"))

    def test_qa_deliverable_allowed_with_review(self):
        plan, projects = self.fixture()
        self.assertEqual(validate_plan(plan, projects)["deliverables"], 1)

    def test_status_rewrite_required_without_truncation(self):
        plan, projects = self.fixture()
        for text in ("word " * 25, "Implemented but validation remains…"):
            plan["deliverables"][0]["status"] = text
            with self.assertRaises(ValueError):
                validate_plan(plan, projects)

    def test_ticket_names_and_duplicate_outcomes_rejected(self):
        plan, projects = self.fixture()
        plan["deliverables"][0]["deliverable_name"] = "INS-1 Implemented feature"
        with self.assertRaises(ValueError):
            validate_plan(plan, projects)
        plan, projects = self.fixture()
        plan["deliverables"].append(copy.deepcopy(plan["deliverables"][0]))
        with self.assertRaises(ValueError):
            validate_plan(plan, projects)

    def test_update_date_is_not_invented_due_date(self):
        self.assertEqual(due_date({"updated": "2026-10-23"}), "")
        plan, projects = self.fixture()
        plan["deliverables"][0]["due_date"] = "2026-10-23"
        with self.assertRaises(ValueError):
            validate_plan(plan, projects)

    def test_month_mismatch_rejected(self):
        plan, projects = self.fixture()
        projects[0]["reporting_period"]["start"] = "2026-09-01"
        with self.assertRaises(ValueError):
            validate_plan(plan, projects)

if __name__ == "__main__":
    unittest.main()
