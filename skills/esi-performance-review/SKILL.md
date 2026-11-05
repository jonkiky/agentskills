---
name: esi-performance-review
description: "Draft ESI manager reviews with the six My Review fields and General Comments, using natural paragraphs that connect each point with its example in casual plain language. Protect reviewer identities in employee-facing comments and include suggestions only when reviewers made them. Align with supplied Leadership Principles. Use for writing, revisions, and authorized HR-form drafts; not ratings or employment decisions."
---

# ESI Performance Review

Produce comments a manager can review and paste into the employee's existing performance-review form. Keep the reusable skill independent of any employee; source documents, evidence notes, and employee drafts belong outside this skill folder.

## Establish the review context

Use the conversation, named source folder, and supplied or visible form to establish the employee, review period, field labels, and selected competency topics. Reuse information already available before asking for it.

For the ESI review form, read [references/esi-form.md](references/esi-form.md). A complete review includes the six My Review competency fields plus General Comments. Include all seven when asked for the full review, while honoring requests limited to particular fields. The live form or user-provided template takes precedence over that reference. Preserve the employee's selected topics unless the user requests a change. If a selected topic is unavailable, propose one with a clear label rather than presenting it as an existing selection.

Look for the standalone ESI Leadership Principles document in the source folder. In this project it is `../ESI Leadership Principles .docx`, relative to this skill folder. Read the definitions and relevant guidance for the selected principles; prefer the detailed document over the short glossary in feedback forms. Its scenarios and failure modes explain the principles, but are not evidence about the employee. If the document is unavailable, use the supplied definitions and state any material limitation without inventing company requirements.

Treat a request to draft, preview, or try the skill as a request to produce reviewable text. When the user also authorizes browser entry, complete the authorized draft entry and verification. Skill invocation alone does not expand the requested destination or authorize submission.

## Select and read the sources

Inventory the specified folder. In folders containing several employees, identify the subject from document contents, not just the filename. A mention of the employee in somebody else's report is only a candidate match. Check the feedback heading and surrounding context before including it.

For local Word feedback, use the included helper with a Python runtime provided by the environment. In Codex desktop, resolve the bundled Python runtime through `load_workspace_dependencies` when needed. The helper uses only the Python standard library.

```sh
python3 scripts/extract_feedback.py --folder /path/to/feedback --employee 'Full Employee Name' --alias 'Known Given Name' --output /path/to/work/feedback-evidence.json
```

The helper searches top-level DOCX files, emits complete body text for candidate documents with paragraph identifiers, and reports exact text duplicates, comments, and extraction warnings. It does not determine whether a document is actually about the employee. Review every selected document in full, including question labels and time qualifiers. Check comments separately; they are not automatically final feedback. If there are tracked changes, images, or other extraction warnings, inspect the relevant original content before relying on it. Use available document-reading tools for other formats.

Retain source filename, reviewer attribution if supported, project, review period if stated, and concrete observations in a separate manager working file. Do not put this source map inside an employee-facing draft or export. Do not infer an author's identity from Word metadata alone. Count duplicate text once. Do not treat template questions or the appended Leadership Principles glossary as employee feedback.

## Build a compact evidence map

Before writing, record each useful claim with its source and the field it best supports. Separate:

- **Peer observation:** An achievement or behavior actually reported in the feedback.
- **Reviewer suggestion:** A request to change or continue a behavior that a reviewer actually made. Record the supporting source passage before including it in a comment.
- **Self-review statement:** The employee's claim or chosen development goal, with independent support identified where present.

Use concrete examples to connect behavior with an explicitly reported result. Preserve qualifiers such as “about,” “overall,” and dependencies on other teams. Keep completed work separate from planned work, and keep each project's status distinct. A future release on one project is not complete because similar work shipped on another.

Prefer specific examples corroborated across sources, while preserving meaningful single-reviewer observations and disagreements. One reviewer mentioning an item does not establish peer consensus. Do not invent metrics, causal benefits, deadlines, career-level requirements, or firsthand manager observations.

An absent topic is an evidence gap, not a weakness. For a selected development topic without peer feedback, a comment may report the employee's stated goal as their own statement, but must not turn it into a reviewer recommendation. Strong evidence of existing capability should be acknowledged; do not manufacture a deficit or new advice to fill an improvement field.

Include suggestions only when a reviewer actually made them. Faithfully paraphrase the requested behavior; do not add a new process, schedule, target, or task because it sounds useful. If there is no reviewer suggestion for a field, omit recommendations and omit any sentence announcing that there were none. Keep that absence in manager notes if useful. A field labeled “to Improve” does not override this rule.

For a complete review, capture every distinct improvement request and request to continue a useful practice. Give each one a primary destination in the comments. Use the category whose selected topic best fits the substance of the request; a related growth point may follow the achievement in that category. If none of the selected categories fits naturally, include the request in General Comments. Do not drop a valid improvement because the employee's selected topics do not cover it, and do not force it into an unrelated category.

Keep a compact coverage record in manager notes: the reviewer's request, its source, its primary destination, and the paragraph that carries it. Combine duplicate requests without losing meaning. Distinguish requests for growth from requests to keep an existing good practice; neither should be rewritten as an unsupported past failure. General Comments may briefly summarize a growth theme already covered elsewhere, but avoid repeating the same detailed advice in several fields.

## Write the comments consistently

Use this user's preferred format for every field, unless a later instruction changes it:

Write normal paragraphs without bullet points, numbering, or bold lead-in labels. Each paragraph begins with one short sentence summarizing a point, followed immediately by one or two sentences that support that same point. Keep the point and its example together in the same paragraph. Start a new paragraph for the next point.

Do not add a separate opening summary, collect all examples at the end, or use labels such as “Evidence,” “Summary,” or “Suggestion.” The write-up should read naturally. Two or three short paragraphs usually suffice; use fewer when that is all the sources support.

Use a casual, respectful manager voice and vocabulary a high-school reader can follow. Favor short sentences and everyday words, such as “helps,” “checks,” and “takes ownership.” Keep official principle names and necessary technical meaning accurate. Avoid corporate language, jargon-heavy phrases, slang, and exaggerated praise.

Each complete comment must contain at least 100 words, including General Comments. This minimum applies to the body of each field, not to each paragraph, and excludes headings, labels, source notes, and word-count metadata. Aim for roughly 110–150 words to leave a small margin for different counting methods. Expand using relevant source details, the action taken, the supported result, or a clearly identified self-review goal. Do not add filler, repeat the same point, invent facts, or introduce new suggestions to meet the minimum. If the supplied material cannot support the length, explain the evidence gap to the manager instead of fabricating content. The leading sentence summarizes; the following sentences supply the example or explain the actual reviewer suggestion. Give each major example one primary home.

- **Achievement:** State the demonstrated contribution and follow it with a supporting example. Include a request to continue a practice only if a reviewer made that request.
- **Improvement:** Recognize the current foundation and include relevant reviewer suggestions when present. Present suggestions as future actions rather than past failures. If there is no suggestion, retain supported observations or clearly identified self-review goals without adding advice.

Use the employee's name or established pronouns. Omit reviewer names, other employees' names, source filenames, and explicit attribution that ties a comment to a particular reviewer. Keep verified project names and useful feature names in the comments when they make the work clear. Describe the work directly, for example “On Project A, he checked the release scope,” rather than identifying whose feedback supplied the example. Avoid “I observed” unless the manager supplied that observation.

Write the employee-facing comments directly in the manager's voice. Do not narrate the source material with phrases such as “the feedback describes,” “the feedback notes,” “the feedback recognizes,” “according to the reviewer,” or “the requested next steps.” State the supported behavior, example, or action itself. Keep source attribution in manager notes. Preserve meaningful time limits and uncertainty in natural language, such as “These issues occurred during a short period when he was new and may have improved since.” Removing source phrases must not turn a limited observation into a current fact or an employee's stated goal into a verified result. Do not invent firsthand manager observations.

Preserve enough project context for the example to make sense: name the project where the work happened and the initiative when useful. Mention the project once per example rather than repeating it in every sentence. Generalize unnecessary personal details, such as replacing a colleague's name with “a teammate.” Do not merge work from different projects, apply one project's outcome to another, or remove context so aggressively that the comment becomes vague. Keep detailed reviewer attribution and claim-to-source mappings in the separate manager source map; identify the feedback documents used in the manager-facing delivery note described below. Do not promise that removing reviewer names makes an example impossible to recognize.

Make the writing direct and specific. Avoid generic praise, repeated opening formulas, unsupported superlatives, personal-character judgments, and ratings. Preserve meaningful concerns without intensifying them. Treat workload across projects as a planning and communication issue when that is what the feedback says.

## General Comments

Include General Comments after the six competency fields in a complete review. This is the overall manager write-up: bring together the employee's main contribution, how they support delivery and the team, and the most important growth suggestions actually raised by reviewers. It is also the required home for reviewer improvement requests that do not fit a selected competency topic, such as broader workload or priority coordination when no matching category exists.

Write one or two natural paragraphs with at least 100 words in total, normally aiming for 110–150; add a short paragraph if needed to preserve a distinct uncategorized improvement. Lead with a supported overall observation and connect it to the main work already described. Include reviewer suggestions only where they exist. Do not repeat every example from the six fields, add a rating, invent a new concern, or introduce advice that was not in the feedback. Apply the same plain-language and reviewer-privacy rules.

When entering the form, check the field's actual instructions and length requirements. A displayed counter alone does not establish whether the number is a minimum, a maximum, or a character count. In a chat or local draft, do not invent a form limit.

## Check and deliver

Read the finished draft against the sources and form:

1. Every factual claim traces to a source or the self-review in the separate manager notes.
2. The comments cover the requested fields and respond to their selected topics without forcing unsupported claims.
3. No planned outcome is presented as complete; no outside dependency is recast as an individual failure.
4. Development comments preserve demonstrated strengths and reflect the scope of the original feedback.
5. Each point and its supporting explanation appear together in a normal paragraph, with no bullets, numbering, bold lead-in labels, separate evidence block, or evidence label.
6. Every recommendation traces to an actual reviewer suggestion; fields without suggestions contain no added advice or “no suggestions” note.
7. Employee-facing text and files omit reviewer attribution, other employee names, and source paths, while preserving accurate project context for each example.
8. Language, repetition, length, and time references are consistent.
9. A complete review includes General Comments after the six competency fields, with its own source mapping in manager notes.
10. Every distinct reviewer improvement or continuation request appears in a fitting category or in General Comments, and the manager coverage record points to its location.
11. Count each field's body text before delivery. All seven comments must have at least 100 words, excluding titles and supporting source notes. Keep the counts available for verification; do not paste them into the HR comment fields.
12. Remove source-reporting phrases from the employee-facing prose while retaining dates, observation limits, and uncertainty that affect the meaning.

Deliver the full paste-ready comments in form order, including General Comments for a complete review, either as a linked Markdown (`.md`) file or printed directly in the response. Follow the user's preferred option when stated; otherwise choose either. A `.txt` or `.json` file alone, a summary, or a link to manager notes does not satisfy this delivery requirement. Use field headings to separate the comments, with normal paragraphs within each field.

In the same response, explicitly list the peer/client feedback documents actually used, using their exact filenames or document titles and links when available. Do not substitute a link to the source map for this list. Identify manager notes, self-reviews, and Leadership Principles separately as supporting materials, so they are not counted as peer feedback. If no peer/client feedback was used, say so. Keep this source list in a separate manager-facing note outside the paste-ready comments and outside any employee-facing Markdown file.

Keep the full claim-to-source map, paragraph identifiers, reviewer attribution, and audit details in a separate manager working file for checking or revision. Do not append reviewer-identifying source links to a version intended for the employee. A self-review-only statement should say that it comes from the employee's own review, without adding a note about missing peer comments.

For authorized browser entry, verify the employee and current field labels, inspect existing manager text, and enter each comment into its matching field. Preserve existing content unless replacement was requested. Verify the values after entry and after the authorized save action. Stop and report a concrete mismatch or save failure rather than repeatedly writing into an uncertain form. Follow the user's current scope for saving or submitting; a draft request ends at the draft.
