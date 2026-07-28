#!/usr/bin/env python3
"""Validate structural, documentation, and prompt rules for this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = (
    ".github/copilot-instructions.md",
    ".github/prompts",
    ".github/workflows/ci-validate.yml",
    "contracts",
    "docs/enforcement-matrix.md",
    "playbooks",
    "standards",
    "standards/prompt-driven-development-workflow.md",
    "stacks/java-springboot",
    "stacks/python-fastapi",
    "templates/docs/implementation-plan-template.md",
    "templates/docs/plan-template.md",
    "tooling/scripts",
    "tooling/tests",
)

PLACEHOLDER_PATTERNS = (
    "Add validation steps",
    "Template generator placeholder",
    "Simple generator placeholder",
)

PROHIBITED_ACTIVE_REFERENCES = (
    "FALLBACK_",
    "generate-template.py",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]*]\(([^)]+)\)")
TEXT_SUFFIXES = {
    ".java",
    ".json",
    ".md",
    ".properties",
    ".ps1",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SKIPPED_TOP_LEVEL_DIRECTORIES = {".git", ".copilot", "templates"}


def _is_under(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def _iter_text_files(root: Path, *, include_templates: bool = False) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        relative = path.relative_to(root)
        if any(part == ".git" for part in relative.parts):
            continue
        if not include_templates and relative.parts and relative.parts[0] == "templates":
            continue

        yield path


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def validate_required_paths(
    root: Path = ROOT,
    *,
    required_paths: Iterable[str] = REQUIRED_PATHS,
) -> list[str]:
    """Return errors for mandatory repository paths that do not exist."""
    return sorted(
        f"Missing required path: {relative_path}"
        for relative_path in required_paths
        if not (root / relative_path).exists()
    )


def validate_markdown_links(root: Path = ROOT) -> list[str]:
    """Validate local links in active Markdown documents.

    Template links are skipped because many point to files created only after a
    template is copied into a target repository.
    """
    errors: list[str] = []

    for markdown_file in sorted(root.rglob("*.md")):
        relative_file = markdown_file.relative_to(root)
        if any(part == ".git" for part in relative_file.parts):
            continue
        if relative_file.parts and relative_file.parts[0] == "templates":
            continue

        content = _read_text(markdown_file)
        if content is None:
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in MARKDOWN_LINK.finditer(line):
                target = match.group(1).strip()
                if " " in target and not target.startswith("<"):
                    target = target.split(" ", maxsplit=1)[0]
                target = target.strip("<>")
                target_without_anchor = target.split("#", maxsplit=1)[0]

                if not target_without_anchor:
                    continue
                if target.startswith(("http://", "https://", "mailto:", "#", "{")):
                    continue

                resolved = (markdown_file.parent / target_without_anchor).resolve()
                if not resolved.exists():
                    errors.append(
                        f"{relative_file}:{line_number}: broken link '{target_without_anchor}'"
                    )

    return sorted(errors)


def validate_no_placeholders(root: Path = ROOT) -> list[str]:
    """Reject known placeholder implementation text in active repository files."""
    errors: list[str] = []
    validator_path = (root / "tooling/scripts/validate_repository.py").resolve()

    for path in _iter_text_files(root):
        if path.resolve() == validator_path:
            continue

        content = _read_text(path)
        if content is None:
            continue

        for pattern in PLACEHOLDER_PATTERNS:
            if pattern in content:
                errors.append(
                    f"{path.relative_to(root)} contains placeholder: '{pattern}'"
                )

    return sorted(errors)


def _split_frontmatter(content: str) -> tuple[list[str], list[str]] | None:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], lines[index + 1 :]

    return None


def validate_prompt_files(root: Path = ROOT) -> list[str]:
    """Validate prompt frontmatter conventions used by VS Code prompt files."""
    errors: list[str] = []
    prompts_directory = root / ".github/prompts"
    if not prompts_directory.exists():
        return errors

    for prompt_file in sorted(prompts_directory.glob("*.prompt.md")):
        relative_file = prompt_file.relative_to(root)
        content = _read_text(prompt_file)
        if content is None:
            continue

        split = _split_frontmatter(content)
        if split is None:
            errors.append(f"{relative_file}: missing or unterminated frontmatter")
            continue

        frontmatter_lines, body_lines = split
        frontmatter_keys = {
            line.split(":", maxsplit=1)[0].strip()
            for line in frontmatter_lines
            if ":" in line and not line.startswith((" ", "\t"))
        }

        if "description" not in frontmatter_keys:
            errors.append(f"{relative_file}: missing frontmatter field 'description'")
        if "mode" in frontmatter_keys:
            errors.append(f"{relative_file}: deprecated frontmatter field 'mode'")

        if any(line.strip() == "mode: agent" for line in body_lines):
            errors.append(f"{relative_file}: duplicate body metadata 'mode: agent'")

    return sorted(errors)


def validate_prohibited_references(root: Path = ROOT) -> list[str]:
    """Reject stale terminology in active guidance and implementation files."""
    errors: list[str] = []

    for path in _iter_text_files(root):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in {".copilot", ".git", "templates"}:
            continue
        if relative == Path("tooling/scripts/validate_repository.py"):
            continue
        if relative == Path("tooling/tests/test_validate_repository.py"):
            continue

        content = _read_text(path)
        if content is None:
            continue

        for reference in PROHIBITED_ACTIVE_REFERENCES:
            if reference in content:
                errors.append(
                    f"{relative} contains stale reference '{reference}'"
                )

    return sorted(errors)


def validate_repository(root: Path = ROOT) -> list[str]:
    """Run all repository checks and return a deterministic error list."""
    errors = [
        *validate_required_paths(root),
        *validate_markdown_links(root),
        *validate_no_placeholders(root),
        *validate_prompt_files(root),
        *validate_prohibited_references(root),
    ]
    return sorted(set(errors))


def main() -> int:
    errors = validate_repository(ROOT)

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
