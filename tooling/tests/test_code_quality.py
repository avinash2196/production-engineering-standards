"""0.16.0, brief D: the code-quality skill, the domain-skill rules, and their wiring."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREES = [".github", ".claude"]


def skill(tree: str, name: str) -> str:
    return (ROOT / tree / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def rule_row(text: str, rule_id: str) -> str:
    match = re.search(rf"^\| {rule_id} \|.*$", text, re.MULTILINE)
    return match.group(0) if match else ""


class CodeQualitySkillTest(unittest.TestCase):
    def test_skill_holds_precedence_severity_and_rules(self):
        for tree in TREES:
            text = skill(tree, "code-quality")
            self.assertIn("`docs/code-standards.md`", text, tree)
            self.assertIn("Existing conventions win next", text, tree)
            for level in ["**High**", "**Medium**", "**Low**"]:
                self.assertIn(level, text, tree)
            self.assertIn("A justified Medium finding counts as satisfied", text, tree)
            for rule_id in ["SZ1", "SZ2", "SZ3", "SZ4", "NM1", "NM2", "NM3", "NM4", "RU1", "RU2", "RU3", "CM1", "CM3", "CM4"]:
                self.assertTrue(rule_row(text, rule_id), f"{tree}: {rule_id}")
            self.assertNotIn("| CM2 |", text, tree)  # dropped by user decision
            self.assertIn("Test files are exempt", rule_row(text, "SZ1"), tree)

    def test_high_rules_are_marked_high(self):
        high = {
            "code-quality": ["CM3"],
            "observability": ["LG3", "LG5"],
            "java-spring-boot": ["LY1", "LY3"],
            "python-fastapi": ["LY1", "LY3"],
            "api-design": ["AP2"],
        }
        for tree in TREES:
            for name, ids in high.items():
                text = skill(tree, name)
                for rule_id in ids:
                    self.assertTrue(rule_row(text, rule_id).rstrip().endswith("| High |"), f"{tree} {name} {rule_id}")
            self.assertIn("High in PDD", rule_row(skill(tree, "code-review"), "RV2"), tree)

    def test_existing_shape_wins_for_layering(self):
        for tree in TREES:
            for name in ["java-spring-boot", "python-fastapi"]:
                text = skill(tree, name)
                self.assertIn("its existing shape wins", text, f"{tree} {name}")
                self.assertIn("raise it as a decision at Plan review (Medium)", text, f"{tree} {name}")

    def test_rule_owners_apply_code_quality(self):
        for tree in TREES:
            self.assertIn("Apply `code-quality`", skill(tree, "code-review"), tree)
            self.assertIn("The exact code follows `code-quality`", skill(tree, "implementation-planning"), tree)
        for agent in ["planner", "implementation-engineer", "refactoring-engineer", "code-reviewer"]:
            for rel in [f".github/agents/{agent}.agent.md", f".claude/agents/{agent}.md"]:
                self.assertIn("`code-quality`", (ROOT / rel).read_text(encoding="utf-8"), rel)

    def test_instruction_templates_point_to_project_overrides(self):
        for tree in TREES:
            for name in ["claude", "copilot"]:
                rel = f"{tree}/skills/prompt-driven-development/templates/application-{name}-instructions.md"
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("`docs/code-standards.md`, when present", text, rel)
                self.assertIn("the setup command never writes it", text, rel)


if __name__ == "__main__":
    unittest.main()
