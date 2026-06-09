---
name: site-snapshots
description: 'Capture full-page browser snapshots for a sitemap URL list using Playwright. Use when asked to take snapshots, generate screenshot baseline/candidate folders, or collect visual evidence for smoke tests.'
argument-hint: 'Sitemap JSON and output folder (example: sitemap-20260521-180929.json images-baseline)'
user-invocable: true
---

# Site Snapshots

Capture full-page PNG screenshots for each URL in a sitemap JSON file.

## When To Use
- Create baseline images before changes
- Create candidate images after changes
- Gather visual evidence for route-level smoke tests

## Inputs
- Ask user for: sitemap JSON file (array of URLs)
- Ask user for: output image folder

## Input Collection Rule
1. Always ask the user to provide each input value.
2. If user does not provide a value, use defaults:
  - sitemap file: `sitemap.json`
  - output folder: `screenshots`

## Portable Preflight
1. Confirm Node.js and npm:
  - `node -v`
  - `npm -v`
2. Install project dependencies:
  - `npm install`
3. Install Playwright Chromium runtime (portable machines/CI):
  - `npx playwright install chromium`
4. Confirm script exists:
  - `./scripts/capture-images.mjs`

## Procedure
1. Validate prerequisites:
  - Ensure runtime checks passed (`node -v`, `npm -v`).
  - Ensure dependencies are installed (`npm install`).
  - Ensure Playwright browser is installed (`npx playwright install chromium`).
   - Ensure crawl output exists (`sitemap-*.json`).
  - Ensure script exists: `./scripts/capture-images.mjs`.
2. Capture baseline snapshots:
  - `node ./.github/skills/site-snapshots/scripts/capture-images.mjs <sitemap.json> images-baseline`
  - If user input is missing, run:
    - `node ./.github/skills/site-snapshots/scripts/capture-images.mjs sitemap.json screenshots`
3. Capture candidate snapshots (same sitemap):
  - `node ./.github/skills/site-snapshots/scripts/capture-images.mjs <sitemap.json> images-candidate`
4. Verify output counts in both folders before comparison.

## Decision Points
- If some pages fail to capture:
  - Re-run capture for same sitemap (transient network/render issues).
  - Check whether those routes require authentication.
- If filenames differ between runs:
  - Confirm both runs used the same sitemap input file.
- If page render looks incomplete:
  - Re-run at low system load; dynamic pages can vary due to lazy loading.

## Completion Checks
- Script completes and prints save paths.
- Output folder contains PNG files.
- Baseline and candidate folders share expected overlapping filenames.

## Output
- Two comparable image sets (for example `images-baseline/` and `images-candidate/`).
