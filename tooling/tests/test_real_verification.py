"""0.16.2 (brief G): real-system verification asked in requirements and per
milestone, light planning dry runs, real-system evidence, fix diagnosis, and
attempts with stop-and-discuss."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREES = [".github", ".claude"]
PDD = "skills/prompt-driven-development"


def read(tree: str, rel: str) -> str:
    return (ROOT / tree / rel).read_text(encoding="utf-8")


def both_commands(op: str) -> list[str]:
    return [
        (ROOT / f".github/prompts/{op}.prompt.md").read_text(encoding="utf-8"),
        (ROOT / f".claude/commands/{op}.md").read_text(encoding="utf-8"),
    ]


class RequirementsInterviewTest(unittest.TestCase):
    def test_real_system_questions_are_asked_not_decided(self):
        for tree in TREES:
            text = read(tree, "skills/requirements-analysis/SKILL.md")
            for phrase in [
                "## Real-System Verification",
                "a local-development adapter (a product feature",
                "Who deploys it, and how is the deployed revision read?",
                "A fake is never invented.",
                "does the user accept that gap?",
                "Never answer for the user.",
                "`docs/verification-environments.md`",
                "never recommend a cloud provider or service",
            ]:
                self.assertIn(phrase, text, (tree, phrase))

    def test_diagnosis_before_a_fix(self):
        text = read(".github", "skills/requirements-analysis/SKILL.md")
        for phrase in ["## Diagnosis Before a Fix", "**Quick path.**", "Reuse what is already known in the session; read fresh anything that changes", "labelled a hypothesis", "Propose no fix and change no code here"]:
            self.assertIn(phrase, text)

    def test_capture_requirements_applies_both(self):
        for text in both_commands("capture-requirements"):
            self.assertIn("Apply `requirements-analysis` Real-System Verification", text)
            self.assertIn("Apply `requirements-analysis` Diagnosis Before a Fix", text)

    def test_requirements_template_sections(self):
        for tree in TREES:
            text = read(tree, f"{PDD}/templates/requirements.md")
            self.assertIn("## Real-System Verification\n", text)
            self.assertIn("## Diagnosis\n", text)
            self.assertLess(text.index("## Real-System Verification"), text.index("## Decisions Deferred to Later Milestones"))


class PlanTest(unittest.TestCase):
    def test_rule_14_and_evidence_kind(self):
        for tree in TREES:
            text = read(tree, f"{PDD}/plan-rules.md")
            self.assertIn("14. **Verification per milestone.**", text)
            self.assertIn("ask the user to confirm every row that differs from the requirements", text)
            self.assertIn("verified only against a redeploy of that change", text)
            self.assertIn("its evidence kind: real, double, or not proven", text)

    def test_plan_template_and_create_plan(self):
        for tree in TREES:
            text = read(tree, f"{PDD}/templates/Plan.md")
            self.assertIn("## Verification Environment\n", text)
            self.assertLess(text.index("## Verification Environment\n"), text.index("## Execution Status"))
        for text in both_commands("create-plan"):
            self.assertIn("Apply Plan Content Rule 14 (Verification per milestone)", text)

    def test_create_implementation_plan_follows_the_row(self):
        for text in both_commands("create-implementation-plan"):
            self.assertIn("Follow the milestone's row in the Plan's Verification Environment", text)


class DryRunTest(unittest.TestCase):
    def test_dry_run_is_light_and_bounded(self):
        for tree in TREES:
            text = read(tree, "skills/implementation-planning/SKILL.md")
            for phrase in [
                "Never during planning: build a container image, download more than about 500 MB, start a container or cloud resource, deploy, or wait on a background job.",
                "Budget about 10 minutes for the whole dry run.",
                "\"deferred to execution in <that environment>\"",
                "In a revision, re-run only the checks whose files changed",
            ]:
                self.assertIn(phrase, text, (tree, phrase))


class EvidenceAndReviewTest(unittest.TestCase):
    def test_real_system_evidence(self):
        text = read(".github", f"{PDD}/execution.md")
        self.assertIn("### Real-System Evidence", text)
        self.assertIn("the deployed revision or image digest, and the commit it was built from", text)
        self.assertIn("never deploys, starts paid resources, or uses production credentials", text)

    def test_final_review_blocks_double_only_evidence(self):
        for tree in TREES:
            self.assertIn("is a blocking finding", read(tree, f"{PDD}/final-review.md"))
            self.assertIn("double evidence without an accepted gap is a blocking finding", read(tree, f"{PDD}/templates/Final-Review.md"))


class AttemptsTest(unittest.TestCase):
    def test_core_has_attempts_and_escalation(self):
        for tree in TREES:
            text = read(tree, f"{PDD}/SKILL.md")
            for phrase in [
                "## Attempts and Escalation",
                "Inside execution a failed check still stops at once",
                "At most 3 attempts in all, each on a different basis",
                "is not an attempt: stop.",
                "up to 3 times with no change, is not an attempt",
                "**Stop and discuss**",
                "two or three options with a recommendation. Then wait.",
            ]:
                self.assertIn(phrase, text, (tree, phrase))

    def test_fix_work_items_cite_the_diagnosis(self):
        text = read(".github", f"{PDD}/milestone-types.md")
        self.assertIn("the quick-path line or the Diagnosis (`requirements-analysis` Diagnosis Before a Fix)", text)
        self.assertIn("a fix aimed at anything else stops and asks", text)


class InstructionTemplateTest(unittest.TestCase):
    def test_project_context_points_to_verification_environments(self):
        for tree in TREES:
            for tool in ("claude", "copilot"):
                text = read(tree, f"{PDD}/templates/application-{tool}-instructions.md")
                self.assertIn("`docs/verification-environments.md`, when present.", text, (tree, tool))


if __name__ == "__main__":
    unittest.main()
