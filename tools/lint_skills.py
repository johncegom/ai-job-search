#!/usr/bin/env python3
"""Lint the repo's skill files.

Run from anywhere: python tools/lint_skills.py

Auto-detects the agent framework in use:
  - Claude Code  (.claude/ present): checks .claude/skills/*/SKILL.md,
    .claude/commands/*.md, and .claude/settings.json
  - Antigravity  (.agents/ present): checks .agents/skills/*/SKILL.md

Both branches may run if both directories exist (hybrid repos).

Shared checks for every SKILL.md regardless of framework:
- Has YAML frontmatter that parses, with non-empty `name` and `description`
- `allowed-tools` entries of the form `Bash(bun run <path> *)` point at
  files that exist (paths resolve relative to the repo root)

Exit code 0 on success, 1 with a failure list otherwise.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("lint_skills.py requires PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []

# ── Framework detection ────────────────────────────────────────────────────────

HAS_CLAUDE = (ROOT / ".claude").is_dir()
HAS_ANTIGRAVITY = (ROOT / ".agents").is_dir()


# ── Shared skill check (both frameworks) ──────────────────────────────────────

def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def check_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{rel(path)}: missing YAML frontmatter (file must start with ---)")
        return
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{rel(path)}: unterminated YAML frontmatter")
        return
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        errors.append(f"{rel(path)}: frontmatter is not valid YAML: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: frontmatter did not parse to a mapping")
        return
    for key in ("name", "description"):
        if not data.get(key):
            errors.append(f"{rel(path)}: frontmatter missing required key '{key}'")

    allowed = data.get("allowed-tools", "")
    if isinstance(allowed, str):
        for match in re.finditer(r"bun run ([^\s)]+)", allowed):
            target = match.group(1).rstrip("*")
            if not target or target.endswith("/"):
                continue
            # Targets may contain globs (e.g. .agents/skills/*/cli/src/cli.ts);
            # require at least one existing file to match.
            if "*" in target:
                if not list(ROOT.glob(target)) and not list((ROOT / ".agents").glob(target)):
                    errors.append(f"{rel(path)}: allowed-tools glob matches no files: {target}")
            else:
                candidates = [ROOT / target, ROOT / ".agents" / target]
                if not any(c.is_file() for c in candidates):
                    errors.append(f"{rel(path)}: allowed-tools references a missing file: {target}")


# ── Claude Code checks ────────────────────────────────────────────────────────

def check_claude_command(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").lstrip().splitlines()
    first = lines[0] if lines else ""
    if not first.startswith("# /"):
        errors.append(
            f"{rel(path)}: command file must start with a '# /<name>' title "
            f"(found: {first[:50]!r})"
        )


def check_claude_settings() -> None:
    path = ROOT / ".claude" / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f".claude/settings.json: {exc}")
        return
    if not isinstance(data.get("permissions", {}).get("allow"), list):
        errors.append(".claude/settings.json: expected permissions.allow to be a list")


def run_claude_checks() -> tuple[int, int]:
    """Returns (skill_count, command_count)."""
    skills = sorted((ROOT / ".claude").glob("skills/*/SKILL.md"))
    commands = sorted((ROOT / ".claude").glob("commands/*.md"))

    if not skills:
        errors.append("Claude: no SKILL.md files found under .claude/skills/")
    if not commands:
        errors.append("Claude: no command files found under .claude/commands/")

    for skill in skills:
        check_skill(skill)
    for command in commands:
        check_claude_command(command)
    check_claude_settings()

    return len(skills), len(commands)


# ── Antigravity checks ────────────────────────────────────────────────────────

def run_antigravity_checks() -> int:
    """Returns skill_count."""
    skills = sorted(ROOT.glob(".agents/skills/*/SKILL.md"))

    if not skills:
        errors.append("Antigravity: no SKILL.md files found under .agents/skills/")

    for skill in skills:
        check_skill(skill)

    return len(skills)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    if not HAS_CLAUDE and not HAS_ANTIGRAVITY:
        print("lint_skills: ERROR - neither .claude/ nor .agents/ directory found")
        return 1

    summary_parts: list[str] = []

    if HAS_CLAUDE:
        n_skills, n_cmds = run_claude_checks()
        summary_parts.append(f"Claude: {n_skills} skills, {n_cmds} commands")

    if HAS_ANTIGRAVITY:
        n_skills = run_antigravity_checks()
        summary_parts.append(f"Antigravity: {n_skills} skills")

    if errors:
        print(f"lint_skills: {len(errors)} failure(s)")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"lint_skills: OK ({', '.join(summary_parts)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
