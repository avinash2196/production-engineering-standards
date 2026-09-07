from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
ERRORS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def validate_required_structure() -> None:
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
        if not (ROOT / rel).exists():
            error(f"missing required path: {rel}")


def validate_no_legacy_top_level_taxonomy() -> None:
    for name in ["standards", "playbooks", "stacks", "contracts", "templates", "agents"]:
        if (ROOT / name).exists():
            error(f"legacy top-level taxonomy is not allowed: {name}")


def validate_skills() -> None:
    skill_root = ROOT / ".github/skills"
    if not skill_root.is_dir():
        return

    names = set()
    valid_name = re.compile(r"^[a-z0-9-]{1,64}$")

    for directory in sorted(p for p in skill_root.iterdir() if p.is_dir()):
        skill_file = directory / "SKILL.md"
        if not skill_file.exists():
            error(f"{directory.relative_to(ROOT)}: missing SKILL.md")
            continue

        text = skill_file.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            error(f"{skill_file.relative_to(ROOT)}: missing YAML frontmatter")
            continue

        front = match.group(1)
        name_match = re.search(r"^name:\s*(.+)$", front, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+)$", front, re.MULTILINE)

        if not name_match or not desc_match:
            error(f"{skill_file.relative_to(ROOT)}: name and description are required")
            continue

        name = name_match.group(1).strip().strip('"')
        description = desc_match.group(1).strip().strip('"')

        if not valid_name.fullmatch(name):
            error(f"{skill_file.relative_to(ROOT)}: invalid skill name")
        if len(description) > 1024:
            error(f"{skill_file.relative_to(ROOT)}: description exceeds 1024 characters")
        if name != directory.name:
            error(f"{skill_file.relative_to(ROOT)}: skill name must match directory")
        if name in names:
            error(f"duplicate skill name: {name}")

        names.add(name)


def validate_agent_and_prompt_names() -> None:
    agent_root = ROOT / ".github/agents"
    prompt_root = ROOT / ".github/prompts"

    if agent_root.is_dir():
        for path in agent_root.glob("*"):
            if path.is_file() and not path.name.endswith(".agent.md"):
                error(f"invalid agent filename: {path.relative_to(ROOT)}")

    if prompt_root.is_dir():
        for path in prompt_root.glob("*"):
            if path.is_file() and not path.name.endswith(".prompt.md"):
                error(f"invalid prompt filename: {path.relative_to(ROOT)}")


def validate_prompt_agent_bindings() -> None:
    agent_root = ROOT / ".github/agents"
    prompt_root = ROOT / ".github/prompts"

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
            error(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
            continue

        agent_match = re.search(
            r'^agent:\s*"?([^"\n]+)"?$',
            match.group(1),
            re.MULTILINE,
        )
        if agent_match:
            agent = agent_match.group(1).strip()
            if agent not in built_in and agent not in agents:
                error(f"{path.relative_to(ROOT)}: unknown agent binding: {agent}")


def validate_markdown_links() -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue

            target_path = target.split("#", 1)[0]
            if not target_path:
                continue

            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                error(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
                continue

            if not resolved.exists():
                error(f"{path.relative_to(ROOT)}: broken relative link: {target}")


def validate_portability() -> None:
    # Placeholder paths such as C:\Users\<name>\... and /Users/<name>/...
    # are valid documentation examples. Concrete machine-specific paths are not.
    windows_abs = re.compile(r"\b[A-Za-z]:\\")
    unix_user_abs = re.compile(r"/(?:Users|home)/[^/\s]+")

    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")

        for line_number, line in enumerate(text.splitlines(), start=1):
            # Allow documented placeholders such as <name>, <user>, or <project>.
            if re.search(r"<[^>]+>", line):
                continue

            if windows_abs.search(line) or unix_user_abs.search(line):
                error(
                    f"{path.relative_to(ROOT)}:{line_number}: "
                    "contains machine-specific absolute path"
                )


def validate_oracle_skill() -> None:
    base = ROOT / ".github/skills/oracle-to-postgres-modernization"
    required = [
        "SKILL.md",
        "references/assessment.md",
        "references/schema-and-sql-mapping.md",
        "references/spring-boot-migration.md",
        "references/verification-and-cutover.md",
    ]

    for rel in required:
        if not (base / rel).exists():
            error(f"oracle-to-postgres skill missing: {rel}")

    if not (ROOT / ".github/prompts/migrate-oracle-to-postgres.prompt.md").exists():
        error("missing explicit Oracle-to-PostgreSQL migration prompt")


def validate_pdd_contract() -> None:
    required_prompts = [
        "capture-requirements.prompt.md",
        "create-plan.prompt.md",
        "create-api-contract.prompt.md",
        "create-implementation-plan.prompt.md",
        "generate-tests.prompt.md",
        "implement-approved-plan.prompt.md",
        "refactor-code.prompt.md",
        "review-code.prompt.md",
    ]

    prompt_root = ROOT / ".github/prompts"
    for name in required_prompts:
        if not (prompt_root / name).is_file():
            error(f"missing required PDD prompt: {name}")

    required_templates = [
        ".github/skills/prompt-driven-development/templates/Plan.md",
        ".github/skills/prompt-driven-development/templates/application-copilot-instructions.md",
        ".github/skills/api-design/templates/API-Contract.md",
    ]
    for rel in required_templates:
        if not (ROOT / rel).is_file():
            error(f"missing required PDD template: {rel}")

    pdd_skill = ROOT / ".github/skills/prompt-driven-development/SKILL.md"
    if pdd_skill.is_file():
        text = pdd_skill.read_text(encoding="utf-8")
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
                error(f"{pdd_skill.relative_to(ROOT)}: missing PDD control: {token}")

    requirements_skill = ROOT / ".github/skills/requirements-analysis/SKILL.md"
    if requirements_skill.is_file():
        text = requirements_skill.read_text(encoding="utf-8").lower()
        for token in ["material unresolved", "clarification", "stop", "wait"]:
            if token not in text:
                error(
                    f"{requirements_skill.relative_to(ROOT)}: "
                    f"missing clarification control: {token}"
                )


def main() -> int:
    validate_required_structure()
    validate_no_legacy_top_level_taxonomy()
    validate_skills()
    validate_agent_and_prompt_names()
    validate_prompt_agent_bindings()
    validate_markdown_links()
    validate_portability()
    validate_oracle_skill()
    validate_pdd_contract()

    if ERRORS:
        print("Repository validation FAILED")
        for item in ERRORS:
            print(f"- {item}")
        return 1

    print("Repository validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
