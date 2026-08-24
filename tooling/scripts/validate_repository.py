#!/usr/bin/env python3
"""Validate structural, documentation, prompt, and Agent Skill rules for this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_PATHS = (
    ".github/copilot-instructions.md",
    ".github/agents",
    ".github/prompts",
    ".github/skills",
    ".github/skills/requirements-analysis/SKILL.md",
    ".github/skills/code-review/SKILL.md",
    ".github/workflows/ci-validate.yml",
    "contracts",
    "docs/copilot-customizations.md",
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

BUILTIN_PROMPT_AGENTS = {"agent", "ask", "plan"}
LEGACY_PROMPT_TOOLS = {
    "codebase",
    "createFile",
    "editFiles",
    "problems",
    "readFile",
    "runCommands",
    "searchFiles",
}
PROHIBITED_CUSTOMIZATION_PHRASES = (
    "apply all standards",
    "against all organisation standards",
    "against all organization standards",
    "reference standards (apply all)",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]*]\(([^)]+)\)")
FRONTMATTER_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")
FRONTMATTER_LIST_ITEM = re.compile(r"^ {2,}-\s+(.+)$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AGENT_NAME = SKILL_NAME
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


def _parse_prompt_frontmatter(
    frontmatter_lines: list[str],
    relative_file: Path,
) -> tuple[dict[str, str | list[str]], list[str]]:
    """Parse the YAML subset used by this repository's prompt frontmatter.

    The repository validator intentionally remains dependency-free. Prompt
    metadata uses only top-level scalar fields plus a list-valued ``tools``
    field, so validating this supported subset is sufficient to catch malformed
    frontmatter without pretending to be a general YAML parser.
    """
    metadata: dict[str, str | list[str]] = {}
    errors: list[str] = []
    active_list_key: str | None = None

    for offset, raw_line in enumerate(frontmatter_lines, start=2):
        if not raw_line.strip():
            continue

        if "\t" in raw_line:
            errors.append(
                f"{relative_file}:{offset}: tabs are not supported in prompt frontmatter"
            )
            continue

        if raw_line.startswith(" "):
            if active_list_key is None:
                errors.append(
                    f"{relative_file}:{offset}: unexpected indentation in prompt frontmatter"
                )
                continue

            item_match = FRONTMATTER_LIST_ITEM.fullmatch(raw_line)
            if item_match is None:
                errors.append(
                    f"{relative_file}:{offset}: invalid list item; use '- value'"
                )
                continue

            item = item_match.group(1).strip()
            if not item:
                errors.append(
                    f"{relative_file}:{offset}: prompt frontmatter list item is empty"
                )
                continue

            value = metadata[active_list_key]
            if isinstance(value, list):
                value.append(item)
            continue

        active_list_key = None
        key_match = FRONTMATTER_KEY.fullmatch(raw_line)
        if key_match is None:
            errors.append(
                f"{relative_file}:{offset}: malformed prompt frontmatter entry"
            )
            continue

        key = key_match.group(1)
        raw_value = (key_match.group(2) or "").strip()
        if key in metadata:
            errors.append(
                f"{relative_file}:{offset}: duplicate frontmatter field '{key}'"
            )
            continue

        if not raw_value:
            metadata[key] = []
            active_list_key = key
        else:
            metadata[key] = raw_value

    return metadata, errors


def _is_inline_list(value: str) -> bool:
    stripped = value.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def _normalize_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _metadata_list_items(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return [_normalize_scalar(item) for item in value]
    if not _is_inline_list(value):
        return []
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [_normalize_scalar(item) for item in inner.split(",") if item.strip()]


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
        metadata, syntax_errors = _parse_prompt_frontmatter(
            frontmatter_lines,
            relative_file,
        )
        errors.extend(syntax_errors)
        if syntax_errors:
            continue

        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{relative_file}: missing frontmatter field 'description'")

        if "mode" in metadata:
            errors.append(f"{relative_file}: deprecated frontmatter field 'mode'")

        agent = metadata.get("agent")
        normalized_agent: str | None = None
        if agent is not None:
            if not isinstance(agent, str) or not agent.strip():
                errors.append(f"{relative_file}: frontmatter field 'agent' must not be empty")
            else:
                normalized_agent = _normalize_scalar(agent)
                if normalized_agent not in BUILTIN_PROMPT_AGENTS:
                    agent_file = root / ".github/agents" / f"{normalized_agent}.agent.md"
                    if not agent_file.exists():
                        errors.append(
                            f"{relative_file}: custom prompt agent '{normalized_agent}' does not exist at .github/agents/{normalized_agent}.agent.md"
                        )

        tools = metadata.get("tools")
        if tools is not None:
            if isinstance(tools, list):
                if not tools:
                    errors.append(
                        f"{relative_file}: frontmatter field 'tools' must contain at least one tool"
                    )
            elif not _is_inline_list(tools):
                errors.append(
                    f"{relative_file}: frontmatter field 'tools' must be a YAML list"
                )

            tool_items = _metadata_list_items(tools) if isinstance(tools, (str, list)) else []
            for tool in tool_items:
                if tool in LEGACY_PROMPT_TOOLS:
                    errors.append(
                        f"{relative_file}: legacy prompt tool '{tool}' is not allowed; use current tool-set/tool identifiers"
                    )
            if normalized_agent and normalized_agent not in BUILTIN_PROMPT_AGENTS:
                errors.append(
                    f"{relative_file}: prompt bound to custom agent '{normalized_agent}' must not override its tools"
                )

        if any(line.strip() == "mode: agent" for line in body_lines):
            errors.append(f"{relative_file}: duplicate body metadata 'mode: agent'")

    return sorted(set(errors))


def validate_instruction_files(root: Path = ROOT) -> list[str]:
    """Validate path-specific instruction structure and repository scoping policy."""
    errors: list[str] = []
    instructions_directory = root / ".github/instructions"
    if not instructions_directory.exists():
        return errors

    for instruction_file in sorted(path for path in instructions_directory.rglob("*") if path.is_file()):
        relative_file = instruction_file.relative_to(root)
        if not instruction_file.name.endswith(".instructions.md"):
            errors.append(
                f"{relative_file}: path-specific instruction files must use '*.instructions.md'"
            )
            continue

        content = _read_text(instruction_file)
        if content is None:
            continue
        split = _split_frontmatter(content)
        if split is None:
            errors.append(f"{relative_file}: missing or unterminated frontmatter")
            continue

        frontmatter_lines, _ = split
        metadata, syntax_errors = _parse_prompt_frontmatter(frontmatter_lines, relative_file)
        errors.extend(syntax_errors)
        if syntax_errors:
            continue

        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{relative_file}: missing frontmatter field 'description'")

        apply_to = metadata.get("applyTo")
        if not isinstance(apply_to, str) or not apply_to.strip():
            errors.append(f"{relative_file}: missing frontmatter field 'applyTo'")
        else:
            normalized = _normalize_scalar(apply_to)
            if normalized in {"**", "**/*"}:
                errors.append(
                    f"{relative_file}: repository-global applyTo '{normalized}' is not allowed; use .github/copilot-instructions.md for repository-wide guidance"
                )

    return sorted(set(errors))


def validate_customization_governance(root: Path = ROOT) -> list[str]:
    """Reject legacy or blanket semantics in active Copilot customization files."""
    errors: list[str] = []
    targets = [root / ".github/copilot-instructions.md"]
    for directory_name in ("agents", "instructions", "prompts", "skills"):
        directory = root / ".github" / directory_name
        if directory.exists():
            targets.extend(path for path in directory.rglob("*.md") if path.is_file())

    for path in sorted(set(targets)):
        if not path.exists():
            continue
        content = _read_text(path)
        if content is None:
            continue
        relative = path.relative_to(root)
        lowered = content.lower()
        for phrase in PROHIBITED_CUSTOMIZATION_PHRASES:
            if phrase in lowered:
                errors.append(
                    f"{relative}: blanket customization phrase is not allowed: '{phrase}'"
                )
        for match in re.finditer(r"`agents/[^`]+\.md`", content):
            errors.append(
                f"{relative}: legacy root-agent reference is not allowed: {match.group(0)}"
            )

    return sorted(set(errors))


def validate_skill_files(root: Path = ROOT) -> list[str]:
    """Validate repository Agent Skill structure and required metadata."""
    errors: list[str] = []
    skills_directory = root / ".github/skills"
    if not skills_directory.exists():
        return errors

    for skill_directory in sorted(path for path in skills_directory.iterdir() if path.is_dir()):
        skill_file = skill_directory / "SKILL.md"
        relative_directory = skill_directory.relative_to(root)
        if not skill_file.exists():
            errors.append(f"{relative_directory}: missing SKILL.md")
            continue

        relative_file = skill_file.relative_to(root)
        content = _read_text(skill_file)
        if content is None:
            continue
        split = _split_frontmatter(content)
        if split is None:
            errors.append(f"{relative_file}: missing or unterminated frontmatter")
            continue

        frontmatter_lines, _ = split
        metadata, syntax_errors = _parse_prompt_frontmatter(
            frontmatter_lines,
            relative_file,
        )
        errors.extend(syntax_errors)
        if syntax_errors:
            continue

        name = metadata.get("name")
        description = metadata.get("description")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{relative_file}: missing frontmatter field 'name'")
        else:
            normalized_name = name.strip().strip('"').strip("'")
            if not SKILL_NAME.fullmatch(normalized_name):
                errors.append(
                    f"{relative_file}: skill name '{normalized_name}' must use lowercase letters, numbers, and hyphens"
                )
            if normalized_name != skill_directory.name:
                errors.append(
                    f"{relative_file}: skill name '{normalized_name}' must match directory '{skill_directory.name}'"
                )

        if not isinstance(description, str) or not description.strip():
            errors.append(f"{relative_file}: missing frontmatter field 'description'")

    return sorted(set(errors))



def validate_agent_files(root: Path = ROOT) -> list[str]:
    """Validate the repository's GitHub Copilot custom-agent profiles."""
    errors: list[str] = []
    agents_directory = root / ".github/agents"
    if not agents_directory.exists():
        return errors

    for agent_file in sorted(path for path in agents_directory.iterdir() if path.is_file()):
        relative_file = agent_file.relative_to(root)
        if not agent_file.name.endswith(".agent.md"):
            errors.append(
                f"{relative_file}: custom-agent files must use the repository convention '*.agent.md'"
            )
            continue

        content = _read_text(agent_file)
        if content is None:
            continue
        split = _split_frontmatter(content)
        if split is None:
            errors.append(f"{relative_file}: missing or unterminated frontmatter")
            continue

        frontmatter_lines, _ = split
        metadata, syntax_errors = _parse_prompt_frontmatter(
            frontmatter_lines,
            relative_file,
        )
        errors.extend(syntax_errors)
        if syntax_errors:
            continue

        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{relative_file}: missing frontmatter field 'description'")

        name = metadata.get("name")
        if name is not None:
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{relative_file}: frontmatter field 'name' must not be empty")
            else:
                normalized_name = name.strip().strip('"').strip("'")
                if not AGENT_NAME.fullmatch(normalized_name):
                    errors.append(
                        f"{relative_file}: agent name '{normalized_name}' must use lowercase letters, numbers, and hyphens"
                    )
                expected_name = agent_file.name.removesuffix(".agent.md")
                if normalized_name != expected_name:
                    errors.append(
                        f"{relative_file}: agent name '{normalized_name}' must match filename '{expected_name}.agent.md'"
                    )

        tools = metadata.get("tools")
        if tools is not None:
            if isinstance(tools, list):
                if not tools:
                    errors.append(
                        f"{relative_file}: frontmatter field 'tools' must contain at least one tool"
                    )
            elif not _is_inline_list(tools):
                errors.append(
                    f"{relative_file}: frontmatter field 'tools' must be a YAML list"
                )

    return sorted(set(errors))


def validate_no_legacy_agents_directory(root: Path = ROOT) -> list[str]:
    """Reject the superseded top-level agents/ convention."""
    legacy = root / "agents"
    if legacy.exists():
        return [
            "Legacy top-level agents/ directory is not allowed; use .github/agents/*.agent.md"
        ]
    return []


def validate_repository_hygiene(root: Path = ROOT) -> list[str]:
    """Reject common IDE/test/cache artifacts from the distributable repository tree."""
    errors: list[str] = []
    forbidden_directories = {".idea", ".pytest_cache", "__pycache__"}

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part == ".git" for part in relative.parts):
            continue
        if path.is_dir() and path.name in forbidden_directories:
            errors.append(f"Repository hygiene: remove generated/local directory '{relative}'")
        elif path.is_file() and path.suffix == ".pyc":
            errors.append(f"Repository hygiene: remove generated bytecode '{relative}'")

    return sorted(set(errors))

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
        *validate_instruction_files(root),
        *validate_agent_files(root),
        *validate_skill_files(root),
        *validate_customization_governance(root),
        *validate_no_legacy_agents_directory(root),
        *validate_repository_hygiene(root),
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
