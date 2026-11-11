"""0.16.1 (brief F S7): the PDD skill is a core SKILL.md plus part files, and
each command names the parts it reads up front."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREES = [".github", ".claude"]
PARTS = ["milestone-types.md", "plan-rules.md", "execution.md", "final-review.md"]
HEADING = re.compile(r"^#{2,3} .+$", re.MULTILINE)

LOADS = {
    "capture-requirements": set(),
    "create-plan": {"milestone-types.md", "plan-rules.md"},
    "create-api-contract": {"plan-rules.md"},
    "create-implementation-plan": {"milestone-types.md", "execution.md"},
    "generate-tests": {"milestone-types.md", "execution.md"},
    "implement-approved-plan": {"execution.md"},
    "refactor-code": {"execution.md"},
    "prepare-pr": {"execution.md"},
    "review-code": set(PARTS),
    "review-production-readiness": set(PARTS),
}


def skill_file(tree: str, name: str) -> Path:
    return ROOT / tree / "skills/prompt-driven-development" / name


def command_files(op: str) -> list[Path]:
    return [ROOT / f".github/prompts/{op}.prompt.md", ROOT / f".claude/commands/{op}.md"]


class PddSkillPartsTest(unittest.TestCase):
    def test_parts_exist_and_are_listed_in_the_core(self):
        for tree in TREES:
            core = skill_file(tree, "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Parts", core, tree)
            for part in PARTS:
                self.assertTrue(skill_file(tree, part).is_file(), (tree, part))
                self.assertIn(f"| `{part}` |", core, (tree, part))

    def test_each_section_lives_in_exactly_one_file(self):
        for tree in TREES:
            seen = {}
            for name in ["SKILL.md", *PARTS]:
                for heading in HEADING.findall(skill_file(tree, name).read_text(encoding="utf-8")):
                    self.assertNotIn(heading, seen, (tree, name, seen.get(heading)))
                    seen[heading] = name

    def test_core_keeps_rules_every_command_needs(self):
        core = skill_file(".github", "SKILL.md").read_text(encoding="utf-8")
        for heading in ["## Lifecycle", "## Work-Item Folders", "## Artifact Authority", "### Approval Status", "### Fresh Context", "## Scope Control"]:
            self.assertIn(heading, core)
        self.assertLess(len(core.split()), 3000)

    def test_parts_hold_the_moved_sections(self):
        expected = {
            "milestone-types.md": ["### OTHER", "### Fix Work Items", "### Adaptive Milestone Decomposition", "### Conditional SETUP / FOUNDATION"],
            "plan-rules.md": ["## Plan Content Rules", "### Changed Contracts"],
            "execution.md": ["## Implementation Plan", "## Test Scope and Output", "## Plan Integrity", "## Plan Progress"],
            "final-review.md": ["## Final Review Authority"],
        }
        for part, headings in expected.items():
            text = skill_file(".github", part).read_text(encoding="utf-8")
            for heading in headings:
                self.assertIn(heading + "\n", text, (part, heading))

    def test_commands_name_the_parts_they_read(self):
        for op, parts in LOADS.items():
            for path in command_files(op):
                text = path.read_text(encoding="utf-8")
                for part in PARTS:
                    if part in parts:
                        self.assertIn(f"`{part}`", text, (path.name, part))
                    else:
                        self.assertNotIn(f"`{part}`", text, (path.name, part))

    def test_changed_contracts_links_point_to_plan_rules(self):
        core = skill_file(".github", "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn('(see "Changed Contracts" below)', core)
        self.assertEqual(core.count("(`plan-rules.md` Changed Contracts)"), 2)


if __name__ == "__main__":
    unittest.main()
