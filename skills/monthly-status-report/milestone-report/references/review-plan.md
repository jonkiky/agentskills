# Reviewed report plan

The agent writes JSON after reviewing explicit source snapshots. Save it in a
task working/output directory, not the reusable skill. Source paths are absolute.
period is YYYY-MM; as_of is the snapshot's actual cutoff date.

Required top-level fields:
- title, version, period, as_of
- sources: absolute source JSON paths
- milestones and deliverables: lists (empty is valid)
- exclusions: optional list of {source_key, reason} for deliberately omitted work

Every row has subproject, status, source_keys (a nonempty list), and evidence
(a prose explanation connecting the result to comments, resolution, and date).
Do not display source_keys or evidence in the DOCX.

Milestone fields:
- milestone: event name without ticket IDs
- delivery_date: YYYY-MM-DD, achieved within the reporting period
- date_basis: explicit event date or recorded completion date, with evidence
- kind: product_release, stage_promotion, major_capability, or major_migration
- significance: why the achieved event is substantial progress

Deliverable fields:
- deliverable_name: completed outcome name without ticket IDs
- due_date: common supported explicit/sprint target or an empty string
- date_updated: latest update among the row's source records
- qualification: implemented, dev_validated, qa_testing, or completed_output

Write statuses as complete summaries of 24 words or fewer. Read older comments
when the latest entry is only Done, a build number, or a closure decision.
Preserve contrary evidence and remaining approval/QA needs. Record important
exclusions so future reviews distinguish deliberate filtering from omissions.

Use each source key for one report outcome; merge repeated loads, a parent and
its implementation tasks, or multiple tasks implementing the same feature.
Different tickets can still duplicate an outcome, so review meaning as well as
keys. Include only records supporting the completed scope; do not pull a blocked
parent into a completed child claim. Name a delivered subcomponent narrowly when
the wider feature remains unfinished.

The validator checks scope, references, dates, duplicate names/keys, known
exclusions, and status length. It does not infer semantic completion or write
summaries. Agent evidence review and rendered page inspection remain necessary.
