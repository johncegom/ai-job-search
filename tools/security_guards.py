#!/usr/bin/env python3
"""Supply-chain guards for the template's riskiest surfaces.

Run from anywhere: python tools/security_guards.py

This repo ships both Antigravity (Gemini) and Claude Code skill files and
CLI code that every fork user executes. These guards make dangerous
changes LOUD, not impossible: a PR that intentionally needs one of them
must update the allowlists in this file in the same diff, so the change
is explicit and reviewable rather than buried.

Checks:
1. .claude/settings.json — the permissions.allow list must not widen
   beyond ALLOWED_PERMISSIONS. Catches a pre-approved command surface
   quietly growing to something like `Bash(*)` or `Bash(curl:*)` that
   every fork user then inherits without review. Antigravity has no
   settings.json equivalent - it manages permissions through the IDE,
   so this check only applies to the Claude Code harness.
2. .gitignore — the personal-data ignore rules must all still be present.
   Catches weakening that would make future users silently commit their
   tracker, profile exports, or application archives.
3. .agents/**/package.json — no npm/bun lifecycle scripts (preinstall,
   install, postinstall, prepare, prepack) and no trustedDependencies.
   Catches code execution smuggled into `bun install`.

Stdlib only. Exit 0 on success, 1 with a failure list otherwise.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []

# The CLI commands and skills the template intends to pre-approve for fork
# users on Claude Code, validated against .claude/settings.json below.
# Antigravity (Gemini) manages permissions through the IDE rather than a
# settings.json file, so it has no equivalent enforcement - this set is the
# single source of truth for the intended safe command surface on both
# harnesses. Any PR that wants to widen it must update this set in the
# same diff.
ALLOWED_PERMISSIONS = {
    "Skill(job-application-assistant)",
    "Bash(bun run:*)",
    "Bash(python salary_lookup.py:*)",
    "Bash(python3 salary_lookup.py:*)",
    "Bash(pdftotext:*)",
}

# Personal-data ignore rules that must never disappear from .gitignore.
REQUIRED_IGNORE_RULES = [
    "salary_data.json",
    "job_scraper/seen_jobs.json",
    "cv/main_*.tex",
    "!cv/main_example.tex",
    "cover_letters/cover_*.tex",
    "documents/cv/**",
    "documents/linkedin/**",
    "documents/diplomas/**",
    "documents/references/**",
    "documents/applications/**",
    "job_search_tracker.csv",
]

FORBIDDEN_SCRIPTS = {"preinstall", "install", "postinstall", "prepare", "prepack"}


def check_permissions() -> None:
    # Antigravity (Gemini) manages permissions through the IDE - there is no
    # settings.json equivalent to scan for that harness. Claude Code does
    # ship .claude/settings.json, so that file is validated against
    # ALLOWED_PERMISSIONS: every fork user inherits whatever it pre-approves.
    path = ROOT / ".claude" / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        errors.append(f".claude/settings.json: unreadable: {exc}")
        return
    except json.JSONDecodeError as exc:
        errors.append(f".claude/settings.json: invalid JSON: {exc}")
        return
    allow = data.get("permissions", {}).get("allow", [])
    extra = sorted(set(allow) - ALLOWED_PERMISSIONS)
    if extra:
        errors.append(
            f".claude/settings.json: permission(s) {extra} not in the reviewed allowlist. "
            "A PR that intentionally widens the pre-approved command surface must add the "
            "entry to ALLOWED_PERMISSIONS in tools/security_guards.py in the same diff."
        )


def check_gitignore() -> None:
    path = ROOT / ".gitignore"
    try:
        rules = {line.strip() for line in path.read_text(encoding="utf-8").splitlines()}
    except OSError as exc:
        errors.append(f".gitignore: unreadable: {exc}")
        return
    for rule in REQUIRED_IGNORE_RULES:
        if rule not in rules:
            errors.append(
                f".gitignore: required personal-data rule missing: {rule!r}. "
                "These rules keep fork users from committing personal data. If the rule moved "
                "or was renamed intentionally, update REQUIRED_IGNORE_RULES in "
                "tools/security_guards.py in the same PR."
            )


def check_package_manifests() -> None:
    manifests = [
        p for p in ROOT.glob(".agents/**/package.json") if "node_modules" not in p.parts
    ]
    if not manifests:
        errors.append(".agents: no package.json files found - glob roots are wrong or the tree moved")
    for manifest in manifests:
        relpath = manifest.relative_to(ROOT)
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{relpath}: unreadable or invalid JSON: {exc}")
            continue
        bad = FORBIDDEN_SCRIPTS & set(data.get("scripts", {}))
        if bad:
            errors.append(
                f"{relpath}: lifecycle script(s) {sorted(bad)} are forbidden - they execute "
                "arbitrary code during `bun install` on every fork user's machine."
            )
        if "trustedDependencies" in data:
            errors.append(
                f"{relpath}: trustedDependencies is forbidden - it re-enables dependency "
                "lifecycle scripts that bun blocks by default."
            )


def main() -> int:
    check_permissions()
    check_gitignore()
    check_package_manifests()
    if errors:
        print(f"security_guards: {len(errors)} failure(s)")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("security_guards: OK (gitignore rules, package manifests)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
