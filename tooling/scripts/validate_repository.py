from __future__ import annotations

from pathlib import Path
import re
import sys

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
        "examples",
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
        name = name_match.group(1).strip()
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
    for path in (ROOT / ".github/agents").glob("*"):
        if path.is_file() and not path.name.endswith(".agent.md"):
            error(f"invalid agent filename: {path.relative_to(ROOT)}")
    for path in (ROOT / ".github/prompts").glob("*"):
        if path.is_file() and not path.name.endswith(".prompt.md"):
            error(f"invalid prompt filename: {path.relative_to(ROOT)}")

def validate_prompt_agent_bindings() -> None:
    agents = {p.name.removesuffix(".agent.md").removesuffix(".md")
              for p in (ROOT / ".github/agents").glob("*.md")}
    built_in = {"ask", "agent", "plan", "edit"}
    for path in (ROOT / ".github/prompts").glob("*.prompt.md"):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            error(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
            continue
        agent_match = re.search(r'^agent:\s*"?([^"\n]+)"?$', match.group(1), re.MULTILINE)
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
    windows_abs = re.compile(r"\b[A-Za-z]:\\\\")
    unix_user_abs = re.compile(r"/Users/[^/\s]+|/home/[^/\s]+")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if windows_abs.search(text) or unix_user_abs.search(text):
            error(f"{path.relative_to(ROOT)}: contains machine-specific absolute path")

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

def main() -> int:
    validate_required_structure()
    validate_no_legacy_top_level_taxonomy()
    validate_skills()
    validate_agent_and_prompt_names()
    validate_prompt_agent_bindings()
    validate_markdown_links()
    validate_portability()
    validate_oracle_skill()

    if ERRORS:
        print("Repository validation FAILED")
        for item in ERRORS:
            print(f"- {item}")
        return 1
    print("Repository validation PASSED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
