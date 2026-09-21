from __future__ import annotations

from pathlib import Path
import re

# The repo root when this script is run directly (CLI entry point only —
# every validation function below takes its root explicitly so the same
# logic can run against a temporary/mutated copy in tests).
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Canonical control block for the "no code change without an approved
# Implementation Plan" rule. This is the single source of truth: every
# persistent instruction file that must enforce this rule carries a
# <!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:START/END --> block whose
# normalized content must match this exactly. Loose keyword matching can
# pass even if a file says the opposite of the rule; comparing against one
# canonical block cannot.
# ---------------------------------------------------------------------------

NO_CODE_CHANGE_CONTROL_ID = "NO-CODE-CHANGE-WITHOUT-APPROVAL"

CANONICAL_NO_CODE_CHANGE_BLOCK = (
    "Every code change must be traceable to a human-approved, "
    "phase-specific Implementation Plan — this applies regardless of "
    "which command, prompt, or free-form request produced the change. "
    "Do not modify production source, tests, configuration, "
    "dependencies, schemas, migrations, scripts, or other executable "
    "repository artifacts from a free-form request, review finding, "
    "failing test, or inferred fix alone.\n"
    "If no approved Implementation Plan authorizes the requested "
    "change, do not implement it; route the work through the "
    "appropriate PDD planning and human-review boundary first.\n"
    "The size and detail of an Implementation Plan should be "
    "proportional to the change — small changes may use a very small "
    "Implementation Plan, but they do not bypass human approval. This "
    "applies to all code changes, not only behavior-changing ones.\n"
    "Documentation-only changes clearly outside executable/code "
    "artifacts may follow the project's normal documentation workflow; "
    "do not invent exceptions to the above for source, tests, "
    "configuration, dependencies, or other executable artifacts."
)

NO_CODE_CHANGE_REQUIRED_FILES = [
    ".github/copilot-instructions.md",
    "CLAUDE.md",
    ".github/skills/prompt-driven-development/templates/application-copilot-instructions.md",
    ".github/skills/prompt-driven-development/templates/application-claude-instructions.md",
]

# ---------------------------------------------------------------------------
# Skill/command environments. Every skill under .github/skills must exist,
# byte-identical, under both mirrors. Populate this only if a specific
# relative path is deliberately allowed to differ or be environment-only —
# do not weaken the comparison itself to work around an unreviewed drift.
# ---------------------------------------------------------------------------

SKILL_MIRROR_ENVIRONMENTS = [".github/skills", ".claude/skills", "plugin/skills"]
SKILL_SYNC_ALLOWED_DIVERGENCES: set[str] = set()

REQUIRED_PDD_OPERATIONS = [
    "capture-requirements",
    "create-plan",
    "create-api-contract",
    "create-implementation-plan",
    "generate-tests",
    "implement-approved-plan",
    "refactor-code",
    "review-code",
]

COMMAND_ENVIRONMENTS = {
    ".github/prompts": "{name}.prompt.md",
    ".claude/commands": "{name}.md",
    "plugin/commands": "{name}.md",
}


def validate_required_structure(root: Path, errors: list[str]) -> None:
    required = [
        ".github/agents",
        ".github/skills",
        ".github/prompts",
        ".github/instructions",
        ".github/workflows",
        "tooling/tests",
        "docs",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")


def validate_no_legacy_top_level_taxonomy(root: Path, errors: list[str]) -> None:
    for name in ["standards", "playbooks", "stacks", "contracts", "templates", "agents"]:
        if (root / name).exists():
            errors.append(f"legacy top-level taxonomy is not allowed: {name}")


def validate_skills(root: Path, errors: list[str]) -> None:
    skill_root = root / ".github/skills"
    if not skill_root.is_dir():
        return

    names = set()
    valid_name = re.compile(r"^[a-z0-9-]{1,64}$")

    for directory in sorted(p for p in skill_root.iterdir() if p.is_dir()):
        skill_file = directory / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{directory.relative_to(root)}: missing SKILL.md")
            continue

        text = skill_file.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append(f"{skill_file.relative_to(root)}: missing YAML frontmatter")
            continue

        front = match.group(1)
        name_match = re.search(r"^name:\s*(.+)$", front, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+)$", front, re.MULTILINE)

        if not name_match or not desc_match:
            errors.append(f"{skill_file.relative_to(root)}: name and description are required")
            continue

        name = name_match.group(1).strip().strip('"')
        description = desc_match.group(1).strip().strip('"')

        if not valid_name.fullmatch(name):
            errors.append(f"{skill_file.relative_to(root)}: invalid skill name")
        if len(description) > 1024:
            errors.append(f"{skill_file.relative_to(root)}: description exceeds 1024 characters")
        if name != directory.name:
            errors.append(f"{skill_file.relative_to(root)}: skill name must match directory")
        if name in names:
            errors.append(f"duplicate skill name: {name}")

        names.add(name)


def _relative_file_set(base: Path) -> dict[str, Path]:
    return {
        p.relative_to(base).as_posix(): p
        for p in base.rglob("*")
        if p.is_file()
    }


def validate_skill_sync(root: Path, errors: list[str]) -> None:
    # Skills are translated verbatim across tool formats (unlike agents/
    # prompts, which legitimately differ in frontmatter and opening
    # structure), so every file under .github/skills must exist, with
    # identical content, under every mirror. Every required environment is
    # checked explicitly below — none of them are allowed to be silently
    # skipped just because a whole tree is missing; a missing tree is itself
    # reported as an error.
    env_paths = {name: root / name for name in SKILL_MIRROR_ENVIRONMENTS}
    missing_envs = [name for name, path in env_paths.items() if not path.is_dir()]
    for name in missing_envs:
        errors.append(f"missing required skill mirror tree: {name}")

    if missing_envs:
        # Can't meaningfully diff file sets against a tree that doesn't
        # exist — the absence itself is already reported above.
        return

    canonical_root = env_paths[".github/skills"]
    canonical_files = _relative_file_set(canonical_root)

    for mirror_name in (".claude/skills", "plugin/skills"):
        mirror_root = env_paths[mirror_name]
        mirror_files = _relative_file_set(mirror_root)

        canonical_rels = set(canonical_files) - SKILL_SYNC_ALLOWED_DIVERGENCES
        mirror_rels = set(mirror_files) - SKILL_SYNC_ALLOWED_DIVERGENCES

        for rel in sorted(canonical_rels - mirror_rels):
            errors.append(
                f"{mirror_name}/{rel}: missing file present in .github/skills/{rel}"
            )

        for rel in sorted(mirror_rels - canonical_rels):
            errors.append(
                f"{mirror_name}/{rel}: unexpected extra file with no counterpart "
                f"in .github/skills — remove it or add it to "
                "SKILL_SYNC_ALLOWED_DIVERGENCES if it is intentionally "
                "environment-specific"
            )

        for rel in sorted(canonical_rels & mirror_rels):
            canonical_text = canonical_files[rel].read_text(encoding="utf-8")
            mirror_text = mirror_files[rel].read_text(encoding="utf-8")
            if canonical_text != mirror_text:
                errors.append(
                    f"{mirror_name}/{rel} has diverged from "
                    f".github/skills/{rel} — skills must stay "
                    "behaviorally identical across .github, .claude, and plugin"
                )


def validate_pdd_commands_across_environments(root: Path, errors: list[str]) -> None:
    # A deleted .claude or plugin command must fail validation just as
    # loudly as a deleted .github prompt — this does not require
    # byte-identical files (environment-specific frontmatter/opening
    # structure legitimately differ), only that the operation exists
    # somewhere in each required environment.
    for env_rel, pattern in COMMAND_ENVIRONMENTS.items():
        env_root = root / env_rel
        if not env_root.is_dir():
            errors.append(f"missing required command directory: {env_rel}")
            continue

        for operation in REQUIRED_PDD_OPERATIONS:
            filename = pattern.format(name=operation)
            if not (env_root / filename).is_file():
                errors.append(
                    f"{env_rel}: missing required PDD command '{operation}' "
                    f"(expected {filename})"
                )


def validate_agent_and_prompt_names(root: Path, errors: list[str]) -> None:
    agent_root = root / ".github/agents"
    prompt_root = root / ".github/prompts"

    if agent_root.is_dir():
        for path in agent_root.glob("*"):
            if path.is_file() and not path.name.endswith(".agent.md"):
                errors.append(f"invalid agent filename: {path.relative_to(root)}")

    if prompt_root.is_dir():
        for path in prompt_root.glob("*"):
            if path.is_file() and not path.name.endswith(".prompt.md"):
                errors.append(f"invalid prompt filename: {path.relative_to(root)}")


def validate_prompt_agent_bindings(root: Path, errors: list[str]) -> None:
    agent_root = root / ".github/agents"
    prompt_root = root / ".github/prompts"

    if not agent_root.is_dir() or not prompt_root.is_dir():
        return

    agents = {
        p.name.removesuffix(".agent.md").removesuffix(".md")
        for p in agent_root.glob("*.md")
    }
    built_in = {"ask", "agent", "plan", "edit"}

    for path in prompt_root.glob("*.prompt.md"):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append(f"{path.relative_to(root)}: missing YAML frontmatter")
            continue

        agent_match = re.search(
            r'^agent:\s*"?([^"\n]+)"?$',
            match.group(1),
            re.MULTILINE,
        )
        if agent_match:
            agent = agent_match.group(1).strip()
            if agent not in built_in and agent not in agents:
                errors.append(f"{path.relative_to(root)}: unknown agent binding: {agent}")


def validate_markdown_links(root: Path, errors: list[str]) -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue

            target_path = target.split("#", 1)[0]
            if not target_path:
                continue

            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes repository: {target}")
                continue

            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken relative link: {target}")


def validate_portability(root: Path, errors: list[str]) -> None:
    # Placeholder paths such as C:\Users\<name>\... and /Users/<name>/...
    # are valid documentation examples. Concrete machine-specific paths are not.
    windows_abs = re.compile(r"\b[A-Za-z]:\\")
    unix_user_abs = re.compile(r"/(?:Users|home)/[^/\s]+")

    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")

        for line_number, line in enumerate(text.splitlines(), start=1):
            # Allow documented placeholders such as <name>, <user>, or <project>.
            if re.search(r"<[^>]+>", line):
                continue

            if windows_abs.search(line) or unix_user_abs.search(line):
                errors.append(
                    f"{path.relative_to(root)}:{line_number}: "
                    "contains machine-specific absolute path"
                )


def validate_oracle_skill(root: Path, errors: list[str]) -> None:
    base = root / ".github/skills/oracle-to-postgres-modernization"
    required = [
        "SKILL.md",
        "references/assessment.md",
        "references/schema-and-sql-mapping.md",
        "references/spring-boot-migration.md",
        "references/verification-and-cutover.md",
    ]

    for rel in required:
        if not (base / rel).exists():
            errors.append(f"oracle-to-postgres skill missing: {rel}")

    if not (root / ".github/prompts/migrate-oracle-to-postgres.prompt.md").exists():
        errors.append("missing explicit Oracle-to-PostgreSQL migration prompt")


def _normalize_control_block(text: str) -> str:
    lines = []
    for line in text.strip("\n").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        lines.append(stripped)
    return "\n".join(lines)


def _extract_control_block(text: str, control_id: str) -> str | None:
    start_marker = f"<!-- PDD-CONTROL:{control_id}:START -->"
    end_marker = f"<!-- PDD-CONTROL:{control_id}:END -->"
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        return None
    return text[start_idx + len(start_marker):end_idx]


def validate_no_code_change_bypass(root: Path, errors: list[str]) -> None:
    # The global authorization boundary ("no code change without an approved
    # Implementation Plan") must survive in every persistent instruction
    # file, independent of which command a user happens to invoke — this is
    # what closes the free-form-prompt bypass a real incident exploited.
    # Compared as a canonical block, not loose keywords: keyword presence
    # can pass even if a file asserts the opposite of the rule.
    canonical_normalized = _normalize_control_block(CANONICAL_NO_CODE_CHANGE_BLOCK)

    for rel in NO_CODE_CHANGE_REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required persistent instruction file: {rel}")
            continue

        text = path.read_text(encoding="utf-8")
        block = _extract_control_block(text, NO_CODE_CHANGE_CONTROL_ID)
        if block is None:
            errors.append(
                f"{rel}: missing or malformed "
                f"PDD-CONTROL:{NO_CODE_CHANGE_CONTROL_ID} block"
            )
            continue

        if _normalize_control_block(block) != canonical_normalized:
            errors.append(
                f"{rel}: PDD-CONTROL:{NO_CODE_CHANGE_CONTROL_ID} block "
                "content diverges from the canonical rule"
            )


def validate_pdd_contract(root: Path, errors: list[str]) -> None:
    required_prompts = [f"{op}.prompt.md" for op in REQUIRED_PDD_OPERATIONS]

    prompt_root = root / ".github/prompts"
    for name in required_prompts:
        if not (prompt_root / name).is_file():
            errors.append(f"missing required PDD prompt: {name}")

    required_templates = [
        ".github/skills/prompt-driven-development/templates/Plan.md",
        ".github/skills/prompt-driven-development/templates/application-copilot-instructions.md",
        ".github/skills/prompt-driven-development/templates/application-claude-instructions.md",
        ".github/skills/api-design/templates/API-Contract.md",
    ]
    for rel in required_templates:
        if not (root / rel).is_file():
            errors.append(f"missing required PDD template: {rel}")

    pdd_skill = root / ".github/skills/prompt-driven-development/SKILL.md"
    if pdd_skill.is_file():
        # Normalize spacing around "/" so "API / External Contract" and
        # "API/External Contract" both satisfy the same required-token check.
        text = re.sub(r"\s*/\s*", "/", pdd_skill.read_text(encoding="utf-8"))
        for token in [
            "Requirements",
            "Plan",
            "Human Review",
            "API/External Contract",
            "RED",
            "GREEN",
            "REFACTOR",
            "Artifact Authority",
            "separate authorization boundaries",
        ]:
            if token not in text:
                errors.append(f"{pdd_skill.relative_to(root)}: missing PDD control: {token}")

    requirements_skill = root / ".github/skills/requirements-analysis/SKILL.md"
    if requirements_skill.is_file():
        text = requirements_skill.read_text(encoding="utf-8").lower()
        for token in ["material unresolved", "clarification", "stop", "wait"]:
            if token not in text:
                errors.append(
                    f"{requirements_skill.relative_to(root)}: "
                    f"missing clarification control: {token}"
                )


VALIDATORS = [
    validate_required_structure,
    validate_no_legacy_top_level_taxonomy,
    validate_skills,
    validate_skill_sync,
    validate_pdd_commands_across_environments,
    validate_agent_and_prompt_names,
    validate_prompt_agent_bindings,
    validate_markdown_links,
    validate_portability,
    validate_oracle_skill,
    validate_pdd_contract,
    validate_no_code_change_bypass,
]


def validate_repository(root: Path) -> list[str]:
    """Run every validator against `root` and return the list of error
    strings (empty if the repository at `root` satisfies the contract).
    Clean state every call — no shared/global mutable state — so this can
    run repeatedly against different (including temporary/mutated) roots
    within the same process, which is what the test suite relies on."""
    errors: list[str] = []
    for validator in VALIDATORS:
        validator(root, errors)
    return errors


def main() -> int:
    errors = validate_repository(REPO_ROOT)

    if errors:
        print("Repository validation FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Repository validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
