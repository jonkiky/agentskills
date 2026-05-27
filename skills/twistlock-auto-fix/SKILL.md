---
name: twistlock-auto-fix
description: "Remediate Twistlock/Prisma Cloud Compute Critical and High container vulnerabilities by having an AI coding agent scan images, inspect the target repo, apply minimal Docker/base-image/OS-package/dependency fixes, build, test, rescan, and repeat until the security gate passes or human review is required."
---

# Twistlock Auto-Fix

Use this skill when the user wants an AI coding agent, such as Codex or Cursor, to directly fix container vulnerabilities reported by Twistlock / Prisma Cloud Compute.

Scanning is evidence and verification. The main job is to edit the target application repository safely.

## Required Inputs

- Target repository path.
- Installed skill path containing `scripts/run_twistlock.sh`; if unknown, search for `skills/twistlock-auto-fix`.
- One or more target image refs, or build/tag commands that produce them.
- Twistlock token via `TWISTLOCK_TOKEN`; avoid username/password.
- Build, test, and optional smoke commands.
- Policy gate; default is zero Critical/High findings.
- Max iterations; default is 3.

## Security Rules

- Never print, write, commit, or include tokens/passwords in reports or PRs.
- Do not suppress, ignore, downgrade, or hide scanner findings as a fix.
- Do not modify business logic without human approval.
- Autonomous changes are limited to:
  - Docker/base image patch or minor updates.
  - OS package fixed-version updates from vendor/distro channels.
  - Dependency manifest and lockfile patch or minor upgrades.
- Stop for major runtime upgrades, ambiguous compatibility, missing fixed-version evidence, repeated failures, or unavailable validation.

## Workflow

1. **Inspect the target repo**
   - Check `git status --short`.
   - Identify Dockerfiles, package manifests, lockfiles, CI/build scripts, image naming, and validation commands.

2. **Run the baseline Twistlock scan**

```bash
mkdir -p .twistlock-runs/baseline
TWISTLOCK_REPORT_DIR=.twistlock-runs/baseline \
TWISTLOCK_TOKEN="$TWISTLOCK_TOKEN" \
skills/twistlock-auto-fix/scripts/run_twistlock.sh \
  -i 'registry.example.com/app:tag'
```

For multiple images, repeat `-i`. If the skill is installed outside the repo root, use the absolute path to `skills/twistlock-auto-fix/scripts/run_twistlock.sh`.

3. **Extract Critical/High findings**

```bash
python3 skills/twistlock-auto-fix/scripts/extract_twistlock_findings.py \
  .twistlock-runs/baseline
```

If the helper is unavailable, read `.twistlock-runs/baseline/*/detailed.json` directly and filter Critical/High findings. If the helper lives in the scanner repo instead, run `${TWISTLOCK_SCANNER_REPO}/scripts/extract_twistlock_findings.py`.

4. **Classify findings**
   - `base_image_or_os_package`
   - `application_dependency`
   - `unknown_manual_review`

5. **Choose the smallest safe fix**
   - Base image: nearest supported compatible patch/minor tag.
   - OS package: fixed version from the distro/vendor package channel.
   - Direct app dependency: patch/minor version that fixes the CVE.
   - Transitive app dependency: upgrade the parent dependency first; use ecosystem-supported override/resolution only when needed.
   - If Twistlock does not expose fixed-version evidence, write a no-fix/manual-review note instead of guessing.

6. **Apply changes**
   - Edit only the files required for the fix.
   - Prefer Dockerfiles, package manifests, lockfiles, and narrowly required compatibility files.
   - Avoid unrelated refactors.

7. **Validate**
   - Run tests.
   - Build the image.
   - Run smoke checks when available.
   - If validation fails, attempt a narrow correction only when the cause is clear.

8. **Rescan and repeat**

```bash
mkdir -p .twistlock-runs/iteration-1
TWISTLOCK_REPORT_DIR=.twistlock-runs/iteration-1 \
TWISTLOCK_TOKEN="$TWISTLOCK_TOKEN" \
skills/twistlock-auto-fix/scripts/run_twistlock.sh \
  -i 'registry.example.com/app:fixed-tag'
```

Repeat until Critical/High count is zero or a stop condition is hit.

## Stop Conditions

- The fix requires product behavior or feature logic decisions.
- The only apparent fix is a major runtime/framework upgrade.
- No fixed version or remediation evidence is available.
- The same Critical/High finding remains after two reasonable attempts.
- Build/test/smoke validation is missing or fails for unclear reasons.

## Output

Return a concise remediation summary:

- Images scanned.
- Critical/High baseline vs final counts.
- Files changed.
- Fixes applied.
- Validation commands and outcomes.
- Remaining findings and why they require human review.
- Artifact paths under `.twistlock-runs/`.

For formal reporting, use `references/remediation-report-template.md`.
