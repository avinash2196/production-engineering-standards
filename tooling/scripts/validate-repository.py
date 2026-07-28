#!/usr/bin/env python3
"""Validate structural and documentation rules for this standards repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = (
    ".github/copilot-instructions.md",
    ".github/prompts",
    ".github/workflows/ci-validate.yml",
    "contracts",
    "standards",
    "stacks/java-springboot",
    "stacks/python-fastapi",
    "playbooks",
    "templates",
    "tooling/scripts",
)

PLACEHOLDER_PATTERNS = (
    "Add validation steps",
    "Template generator placeholder",
    "Simple generator placeholder",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]*]\(([^)]+)\)")


def validate_required_paths() -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).exists():
            errors.append(f"Missing required path: {relative_path}")

    return errors


def validate_markdown_links() -> list[str]:
    errors: list[str] = []

    for markdown_file in ROOT.rglob("*.md"):
        if ".git" in markdown_file.parts:
            continue

        content = markdown_file.read_text(encoding="utf-8")

        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in MARKDOWN_LINK.finditer(line):
                target = match.group(1).strip().split()[0].strip("<>")
                target = target.split("#", maxsplit=1)[0]

                if not target:
                    continue

                if target.startswith(
                        ("http://", "https://", "mailto:", "#", "{")
                ):
                    continue

                resolved = markdown_file.parent / target

                if not resolved.exists():
                    relative_file = markdown_file.relative_to(ROOT)
                    errors.append(
                        f"{relative_file}:{line_number}: "
                        f"broken link '{target}'"
                    )

    return errors


def validate_no_placeholders() -> list[str]:
    errors: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for pattern in PLACEHOLDER_PATTERNS:
            if pattern in content:
                errors.append(
                    f"{path.relative_to(ROOT)} contains placeholder: "
                    f"'{pattern}'"
                )

    return errors


def main() -> int:
    errors = [
        *validate_required_paths(),
        *validate_markdown_links(),
        *validate_no_placeholders(),
    ]

    if errors:
        print("Repository validation failed:\n")

        for error in errors:
            print(f"- {error}")

        print(f"\n{len(errors)} validation error(s) found.")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())