from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / ".github/prompts"
AGENTS = ROOT / ".github/agents"
INSTRUCTIONS = ROOT / ".github/instructions"

SPECIALIST_PROMPTS = {
    "analyse-codebase": "codebase-analyst",
    "compliance-review": "compliance-reviewer",
    "generate-tests": "test-engineer",
    "implement-approved-plan": "backend-service-engineer",
    "maintenance-check": "maintenance-reviewer",
    "refactor-code": "refactoring-engineer",
    "review-architecture": "architecture-reviewer",
    "review-code": "code-reviewer",
    "review-distributed-systems": "distributed-systems-reviewer",
    "review-hipaa": "hipaa-reviewer",
    "review-production-readiness": "production-readiness-reviewer",
}

LEGACY_PROMPT_TOOLS = {
    "codebase",
    "createFile",
    "editFiles",
    "problems",
    "readFile",
    "runCommands",
    "searchFiles",
}


def frontmatter(text: str) -> str:
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ""
    return parts[1]


def scalar(metadata: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", metadata)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


class CopilotCustomizationSemanticsTest(unittest.TestCase):
    def test_path_specific_instructions_are_never_repository_global(self) -> None:
        failures = []
        for path in sorted(INSTRUCTIONS.glob("*.instructions.md")):
            metadata = frontmatter(path.read_text(encoding="utf-8"))
            apply_to = scalar(metadata, "applyTo")
            if apply_to in {None, "**", "**/*"}:
                failures.append(f"{path.relative_to(ROOT)}: applyTo={apply_to!r}")
        self.assertEqual([], failures)

    def test_specialist_prompts_bind_to_existing_matching_custom_agents(self) -> None:
        failures = []
        for prompt_name, agent_name in SPECIALIST_PROMPTS.items():
            path = PROMPTS / f"{prompt_name}.prompt.md"
            metadata = frontmatter(path.read_text(encoding="utf-8"))
            actual = scalar(metadata, "agent")
            if actual != agent_name:
                failures.append(
                    f"{path.relative_to(ROOT)}: expected agent {agent_name!r}, got {actual!r}"
                )
            agent_file = AGENTS / f"{agent_name}.agent.md"
            if not agent_file.exists():
                failures.append(f"missing {agent_file.relative_to(ROOT)}")
            if re.search(r"(?m)^tools:\s*$", metadata):
                failures.append(
                    f"{path.relative_to(ROOT)}: custom-agent prompt overrides agent tools"
                )
        self.assertEqual([], failures)

    def test_prompt_frontmatter_does_not_use_legacy_tool_identifiers(self) -> None:
        failures = []
        for path in sorted(PROMPTS.glob("*.prompt.md")):
            metadata = frontmatter(path.read_text(encoding="utf-8"))
            for tool in LEGACY_PROMPT_TOOLS:
                if re.search(rf"(?m)^\s*-\s*{re.escape(tool)}\s*$", metadata):
                    failures.append(f"{path.relative_to(ROOT)}: {tool}")
        self.assertEqual([], failures)

    def test_active_customizations_do_not_reference_legacy_root_agents(self) -> None:
        failures = []
        for path in sorted((ROOT / ".github").rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            if re.search(r"`agents/[^`]+\.md`", text):
                failures.append(str(path.relative_to(ROOT)))
        self.assertEqual([], failures)

    def test_analysis_and_maintenance_are_applicability_and_evidence_driven(self) -> None:
        analysis = (PROMPTS / "analyse-codebase.prompt.md").read_text(encoding="utf-8")
        maintenance = (PROMPTS / "maintenance-check.prompt.md").read_text(encoding="utf-8")
        self.assertIn("standards that are actually applicable", analysis)
        self.assertIn("Do not require layers merely because a template contains them", analysis)
        self.assertIn("NEEDS VERIFICATION", analysis)
        self.assertIn("Do **not** invent a universal rule", maintenance)
        self.assertIn("NEEDS POLICY", maintenance)
        self.assertIn("Do not require fixed fields", maintenance)

    def test_hipaa_review_requires_applicability_before_controls(self) -> None:
        prompt = (PROMPTS / "review-hipaa.prompt.md").read_text(encoding="utf-8")
        agent = (AGENTS / "hipaa-reviewer.agent.md").read_text(encoding="utf-8")
        self.assertIn("Step 1 — Establish Applicability", prompt)
        self.assertIn("HIPAA APPLICABILITY: NEEDS VERIFICATION", prompt)
        self.assertIn("Healthcare vocabulary", agent)
        self.assertIn("does not prove HIPAA scope", agent)

    def test_adr_and_document_prompts_do_not_invent_approval(self) -> None:
        adr = (PROMPTS / "generate-adr.prompt.md").read_text(encoding="utf-8")
        create_doc = (PROMPTS / "create-doc.prompt.md").read_text(encoding="utf-8")
        self.assertIn("default to `Proposed`", adr)
        self.assertIn("Use `Accepted` only", adr)
        self.assertIn("Silence is not approval", create_doc)
        self.assertIn("stop", create_doc.lower())

    def test_code_review_skill_has_no_legacy_agent_dependency(self) -> None:
        skill = (ROOT / ".github/skills/code-review/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("`agents/code-reviewer.md`", skill)
        self.assertIn("../../prompts/review-code.prompt.md", skill)
        self.assertNotIn(".github/prompts/review-code.prompt.md", skill)

    def test_all_custom_agents_define_activation_behavior(self) -> None:
        failures = []
        for path in sorted(AGENTS.glob("*.agent.md")):
            text = path.read_text(encoding="utf-8")
            if "## On Activation" not in text:
                failures.append(str(path.relative_to(ROOT)))
        self.assertEqual([], failures)

    def test_agent_and_skill_definitions_have_no_machine_specific_paths(self) -> None:
        failures = []
        machine_path = re.compile(r"(?:[A-Za-z]:[\\/]|/Users/|/home/|/mnt/)")
        paths = list(AGENTS.glob("*.agent.md")) + list((ROOT / ".github/skills").rglob("*.md"))
        for path in sorted(paths):
            text = path.read_text(encoding="utf-8")
            if machine_path.search(text):
                failures.append(str(path.relative_to(ROOT)))
        self.assertEqual([], failures)

    def test_prompt_surface_limitation_is_documented(self) -> None:
        doc = (ROOT / "docs/copilot-customizations.md").read_text(encoding="utf-8")
        self.assertIn("Agent Host sessions do not consume prompt files", doc)
        self.assertIn("Language, stack, or file-path guidance only", doc)


if __name__ == "__main__":
    unittest.main()
