"""0.16.0 step 6: Command Routing in the instruction templates (brief E C28,
C29, C36), fix work items (C27), and the Quickstart wording."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREES = [".github", ".claude"]
TEMPLATES = [
    f"{tree}/skills/prompt-driven-development/templates/application-{tool}-instructions.md"
    for tree in TREES
    for tool in ("claude", "copilot")
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def routing(rel: str) -> str:
    match = re.search(r"^## Command Routing\n(.*?)(?=^## )", read(rel), re.MULTILINE | re.DOTALL)
    assert match, rel
    return match.group(1)


class CommandRoutingTest(unittest.TestCase):
    def test_every_template_has_the_same_fixed_section(self):
        sections = {rel: routing(rel) for rel in TEMPLATES}
        self.assertEqual(len(set(sections.values())), 1)
        for rel, section in sections.items():
            self.assertTrue(section.lstrip().startswith("<!-- FIXED — preserve verbatim -->"), rel)

    def test_routes(self):
        section = routing(TEMPLATES[0])
        for phrase in [
            "| New work, or a change to behavior | `capture-requirements <work-item>`",
            "First list the `docs/.ai/*/Plan.md` files with Pending milestones",
            "the `docs/.ai/*/Final-Review.md` files whose User Decision is empty",
            "A fix work item with one milestone",
            "`prepare-pr <work-item>` after a finished milestone",
            "When no command covers the request, say so, name the closest command, and ask.",
            "Never create status or summary files",
        ]:
            self.assertIn(phrase, section)

    def test_routed_commands_exist_in_both_tools(self):
        names = {n for n in re.findall(r"`([a-z][a-z-]+)(?: [^`]*)?`", routing(TEMPLATES[0])) if "-" in n}
        names.discard("production-engineering-standards")
        self.assertGreaterEqual(len(names), 5)
        for name in names:
            self.assertTrue((ROOT / f".github/prompts/{name}.prompt.md").is_file(), name)
            self.assertTrue((ROOT / f".claude/commands/{name}.md").is_file(), name)

    def test_templates_show_prepare_pr_in_the_lifecycle(self):
        for rel in TEMPLATES:
            self.assertIn("prepare-pr: review → Human go → commit and draft pull request", read(rel), rel)


class FixWorkItemTest(unittest.TestCase):
    def test_pdd_skill_defines_fix_work_items(self):
        for tree in TREES:
            pdd = read(f"{tree}/skills/prompt-driven-development/SKILL.md")
            self.assertIn("### Fix Work Items", pdd, tree)
            self.assertIn("the defect, the expected behavior, and how to reproduce it", pdd, tree)
            self.assertIn("RED still proves the defect first", pdd, tree)
            self.assertIn("nothing is approved automatically because it is small", pdd, tree)

    def test_capture_requirements_handles_a_fix(self):
        for rel in [".github/prompts/capture-requirements.prompt.md", ".claude/commands/capture-requirements.md"]:
            self.assertIn("For a fix work item (`prompt-driven-development` Fix Work Items)", read(rel), rel)


class QuickstartTest(unittest.TestCase):
    def test_setup_command_and_commands_per_phase(self):
        readme = read("README.md")
        self.assertIn("It must come from the setup command; never write it by hand", readme)
        self.assertIn("Start every phase with a command and the work-item name", readme)
        guide = read("docs/getting-started.md")
        self.assertIn("Always generate the file with the setup command; never write it by hand.", guide)
        self.assertIn("Start every phase with its command and the work-item name.", guide)


if __name__ == "__main__":
    unittest.main()
