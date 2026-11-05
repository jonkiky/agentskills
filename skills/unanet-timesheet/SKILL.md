---
name: unanet-timesheet
description: Fill and save the user's Essential Software Unanet timesheet through Chrome, using their default project allocation or explicitly requested hours. Use for daily timesheet entry and scheduled timesheet runs, not timesheet approval or submission.
---

# Unanet timesheet

Enter hours for the requested date at https://essential-soft.unanet.biz/essential-soft/action/time using the user's Chrome browser and the available browser-control tools. Follow their current tool documentation. Do not store credentials in this skill or extract browser secrets.

## Date and allocation

- Interpret dates in America/New_York. For a scheduled run, use the trigger's local calendar date. For “yesterday,” use the preceding calendar date; do not silently substitute a business day. If no date is supplied, use today in that timezone.
- Routine scheduled entries apply to weekdays. Ask before filling an explicitly requested weekend if the intended allocation is unclear. Do not backfill other dates without a request.
- Unless the user specifies different hours, use F23-cBioPortal: 2 hours; F23-DataCentric: 2 hours; F23-AI: 4 hours, totaling 8.
- The observed project is F23-CCDI_OY4. DataCentric is displayed as F23-DataCentric(Federation). Confirm current project/task labels in the live page. Numeric task prefixes and row order can change; never identify tasks from a prior row index alone. Ask if the project or task is missing or ambiguous rather than charging a substitute.

## Open and inspect

1. Open the Time dashboard in Chrome. Use the signed-in session or click Login when credentials are prefilled. Clicking the Username field may activate Chrome autofill. If credentials remain absent or additional authentication is needed, leave the login page available and report the blocker.
2. Under Active Timesheets, edit the period containing the target date. Never reuse a stored timesheet key: the original key 3719 belongs to April 2024. Check the displayed date range and status.
3. If the period has no timesheet, use Create Timesheet with the target date and Save to create it. Confirm its date range before entering hours. Creating a new period can prepopulate holiday hours; preserve those entries.
4. If the timesheet is submitted, approved, locked, or controlled by another person, stop and report that state. Do not recall, unlock, or submit it.
5. Inspect every row for the target date, including holiday and leave rows. If the desired allocation already exists exactly, leave it unchanged. If any existing nonblank/nonzero entries conflict with the requested allocation, ask before changing them. This includes holiday or leave hours on the target date. For a partial exact match with no other hours, fill only the missing default entries.

## Fill, save, verify

- Map the target date column and current task rows from the visible table. Previously observed input IDs follow `d_r<row>_<zero-based-day-offset>`, but use them only after confirming current DOM labels and IDs. Do not assume a month always begins at offset zero; periods may start midmonth.
- Enter the missing values in the matching date cells. Move focus out of the last edited cell so the daily total recalculates. Check that the target day totals 8 hours, or the user's explicitly requested total.
- Click **Save** as the final modifying action. Never click **Submit** as part of this skill.
- Verify the returned, reloaded timesheet shows the expected task values, daily total, and in-progress status (typically INUSE). If saving is interrupted or uncertain, inspect persisted entries before retrying; never blindly add hours again.
- Capture a screenshot of the saved result when required by the browser tools, keep the edited tab available, and complete any browser-tool completion reporting.
- Report the full target date, saved task hours and total, and that the timesheet remains in progress. Report conflicts or access/save failures accurately. For heartbeat runs, use the required heartbeat response format; use a quiet result if everything was already correct and no change was needed.

## Scope

Invoking this skill to fill a timesheet authorizes the requested entry and Save workflow; merely creating, reviewing, or editing this skill does not authorize a live timesheet change. A skill does not create a schedule. Preserve existing automation schedules unless the user requests a schedule change.
