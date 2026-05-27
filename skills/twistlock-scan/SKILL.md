---
name: twistlock-scan
description: Scan container images with Prisma Cloud Compute (Twistlock) using twistcli for local images and run_twistlock.sh for remote registry images.
domain: cybersecurity
subdomain: container-security
tags:
- containers
- docker
- twistlock
- prisma-cloud
- vulnerability-scanning
version: '1.0'
author: codex
license: Apache-2.0
nist_csf:
- DE.CM-01
- PR.PS-01
- RS.AN-03
---

# Twistlock Scan

## Overview

This skill standardizes how to scan container images with Prisma Cloud Compute (Twistlock):

- Use `twistcli images scan` for **local Docker images**.
- Use `run_twistlock.sh` for **remote registry images** (on-demand scan + poll for registry results).

## When to Use

- You need a quick local vulnerability check before push/deploy.
- You need registry-backed scan results for a published image tag.
- You want consistent scan commands and output handling.

## Prerequisites

- Access to Prisma Cloud Compute console (e.g., `https://twistlock.nci.nih.gov`).
- One of:
  - `TWISTLOCK_TOKEN`, or
  - `TWISTLOCK_USERNAME` and `TWISTLOCK_PASSWORD`.
- Docker daemon reachable from the scan command.
- `twistcli` binary available in working directory or PATH.

## Local Scan (Preferred for Fast Iteration)

Run this for an image that exists on your local Docker daemon:

```bash
./twistcli images scan \
  --address https://twistlock.nci.nih.gov \
  --user "$TWISTLOCK_USERNAME" \
  --password "$TWISTLOCK_PASSWORD" \
  --details \
  NAME_OF_DOCKER_IMAGE
```

If your Docker daemon is Colima, set the daemon socket first:

```bash
DOCKER_CLIENT_ADDRESS=unix:///Users/<user>/.colima/default/docker.sock \
./twistcli images scan \
  --address https://twistlock.nci.nih.gov \
  --user "$TWISTLOCK_USERNAME" \
  --password "$TWISTLOCK_PASSWORD" \
  --details \
  NAME_OF_DOCKER_IMAGE
```

## Remote Registry Scan

Use this when scanning a registry image tag (`registry/repo:tag`):

```bash
TWISTLOCK_REPORT_DIR=.twistlock-runs/baseline \
./run_twistlock.sh -i '123456789012.dkr.ecr.us-east-1.amazonaws.com/repo:tag'
```

Notes:
- `run_twistlock.sh` expects `registry/repository:tag` format.
- This path relies on registry scan row creation/polling in console.

## Output Expectations

- Local scan prints vulnerability table and summary counts:
  - `critical`, `high`, `medium`, `low`
- Remote scan writes artifacts under `TWISTLOCK_REPORT_DIR` when available.

## Troubleshooting

- `no such image`: image tag not present on current Docker daemon.
- `expired token`: refresh `TWISTLOCK_TOKEN` or use username/password.
- Registry polling timeout: scan was triggered but registry row did not materialize in time.
- `connect /var/run/docker.sock`: point to the correct daemon with `DOCKER_CLIENT_ADDRESS`.

## Safety Rules

- Never commit or print live tokens/passwords.
- Prefer environment variables over inline credentials.
- Treat scan output as sensitive operational data.
