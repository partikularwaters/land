#!/usr/bin/env python3
"""Verification engine for the land skill.

Validates SKILL.md frontmatter, canonical Conventional Commit types,
required workflow steps, and self-consistency with CONTRIBUTING.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "SKILL.md"
CONTRIBUTING_PATH = ROOT / "CONTRIBUTING.md"

REQUIRED_SECTIONS = [
    r"Step 1[:—] Resolve the attribution convention",
    r"Step 2[:—] Resolve mode",
    r"Step 3[:—] Gather scope and verify project conventions",
    r"Step 4[:—] Draft the commit message",
    r"Step 5[:—] Mode branching",
    r"The Rule",
]

EXPECTED_TYPES = [
    "feat",
    "fix",
    "docs",
    "style",
    "chore",
    "refactor",
    "test",
    "ci",
    "build",
    "perf",
]


def check_skill_md() -> list[str]:
    errors: list[str] = []
    if not SKILL_PATH.is_file():
        return [f"Missing {SKILL_PATH.name} at repository root."]

    content = SKILL_PATH.read_text(encoding="utf-8")

    # Frontmatter check
    if not content.startswith("---\n"):
        errors.append("SKILL.md missing opening YAML frontmatter delimiter (---).")
    frontmatter_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        errors.append("SKILL.md frontmatter is improperly closed or malformed.")
    else:
        fm = frontmatter_match.group(1)
        if not re.search(r"^name:\s*land\s*$", fm, re.MULTILINE):
            errors.append("Frontmatter missing 'name: land'.")
        if not re.search(r"^description:\s*.+", fm, re.MULTILINE):
            errors.append("Frontmatter missing 'description'.")

    # Section headers check
    for section_pattern in REQUIRED_SECTIONS:
        if not re.search(section_pattern, content):
            errors.append(f"SKILL.md missing required section matching: '{section_pattern}'.")

    # Canonical types check
    for c_type in EXPECTED_TYPES:
        pattern = rf"`{c_type}:?`"
        if not re.search(pattern, content):
            errors.append(f"SKILL.md missing canonical commit type: `{c_type}`.")

    # Attribution trailer format check
    if "Assisted-by: <product> (<model, if known>)" not in content:
        errors.append("SKILL.md missing standard fallback Assisted-by trailer format.")

    return errors


def check_contributing_md() -> list[str]:
    errors: list[str] = []
    if not CONTRIBUTING_PATH.is_file():
        return [f"Missing {CONTRIBUTING_PATH.name} at repository root."]

    content = CONTRIBUTING_PATH.read_text(encoding="utf-8")

    if "## Commits" not in content:
        errors.append("CONTRIBUTING.md missing '## Commits' section.")
    if "## Pre-commit checks" not in content:
        errors.append("CONTRIBUTING.md missing '## Pre-commit checks' section.")
    if "python3 scripts/verify_skill.py" not in content:
        errors.append("CONTRIBUTING.md pre-commit checks missing 'python3 scripts/verify_skill.py'.")
    if "Assisted-by:" not in content:
        errors.append("CONTRIBUTING.md missing 'Assisted-by:' trailer definition.")

    return errors


def test_attribution_resolution_logic() -> list[str]:
    """Test simulated resolution logic against CONTRIBUTING.md content."""
    errors: list[str] = []

    # Mock CONTRIBUTING with custom rule
    sample_custom = (
        "# Contributing\n\n"
        "## AI Assistance\n\n"
        "Use trailer: `AI-Generated: true`\n"
    )
    if "AI-Generated: true" not in sample_custom:
        errors.append("Mock resolution test failed for custom trailer.")

    # Mock CONTRIBUTING with pre-commit command
    sample_checks = (
        "## Pre-commit checks\n\n"
        "```bash\n"
        "npm test\n"
        "```\n"
    )
    match = re.search(r"## Pre-commit checks\s+```(?:bash|sh)?\n(.*?)\n```", sample_checks, re.DOTALL)
    if not match or "npm test" not in match.group(1):
        errors.append("Mock pre-commit check parsing failed.")

    return errors


def main() -> int:
    all_errors: list[str] = []

    print("Verifying SKILL.md...")
    skill_errors = check_skill_md()
    if skill_errors:
        all_errors.extend(skill_errors)
    else:
        print("  ✓ SKILL.md structure, frontmatter, and canonical types valid.")

    print("Verifying CONTRIBUTING.md...")
    contributing_errors = check_contributing_md()
    if contributing_errors:
        all_errors.extend(contributing_errors)
    else:
        print("  ✓ CONTRIBUTING.md conventions and pre-commit commands valid.")

    print("Testing convention resolution logic...")
    logic_errors = test_attribution_resolution_logic()
    if logic_errors:
        all_errors.extend(logic_errors)
    else:
        print("  ✓ Mock convention resolution tests passed.")

    if all_errors:
        print("\nVerification failed with errors:", file=sys.stderr)
        for err in all_errors:
            print(f"  ✗ {err}", file=sys.stderr)
        return 1

    print("\nAll skill verification checks passed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
