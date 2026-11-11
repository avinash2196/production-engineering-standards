"""0.16.0 step 4: Review Summary (C20), lighter plans (L2-L6), paired plans (P1),
recorded answers (C34), per-command inputs (C37), and test output (P4)."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREES = [".github", ".claude"]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def command_pair(op: str) -> list[str]:
    return [f".github/prompts/{op}.prompt.md", f".claude/commands/{op}.md"]


class ReviewSummaryAndPlanSizeTest(unittest.TestCase):
    def test_review_summary_sits_under_milestone_type(self):
        for tree in TREES:
            template = read(f"{tree}/skills/prompt-driven-development/templates/Implementation-Plan.md")
            self.assertLess(template.index("## Milestone Type"), template.index("## Review Summary"), tree)
            self.assertLess(template.index("## Review Summary"), template.index("## Authoritative References"), tree)
            for field in ["Behavior change:", "Requirements covered:", "Files:", "Tests added:", "Verification:", "Needs attention:"]:
                self.assertIn(field, template, tree)
            skill = read(f"{tree}/skills/implementation-planning/SKILL.md")
            self.assertIn("## Review Summary", skill, tree)
            self.assertIn("It adds no decision", skill, tree)
            self.assertIn("confirm that each line matches the detailed sections", skill, tree)

    def test_plan_size_keeps_exact_code_and_trims_the_rest(self):
        for tree in TREES:
            skill = read(f"{tree}/skills/implementation-planning/SKILL.md")
            self.assertIn("## Plan Size", skill, tree)
            self.assertIn("Keep the exact before and after code in full", skill, tree)
            self.assertIn("No inventory.", skill, tree)
            template = read(f"{tree}/skills/prompt-driven-development/templates/Implementation-Plan.md")
            self.assertIn("No inventory of the repository.", template, tree)
            self.assertIn("Add no section beyond this template unless the milestone needs it", template, tree)
            self.assertIn("### Affected Tests", template, tree)

    def test_dry_run_and_repeat_scope(self):
        for tree in TREES:
            skill = read(f"{tree}/skills/implementation-planning/SKILL.md")
            self.assertIn("RED: compile everything and run only the new tests", skill, tree)
            self.assertIn("The full suite runs once, at execution only.", skill, tree)
            self.assertIn("(only those tests, not the whole suite)", skill, tree)


class TestScopeAndOutputTest(unittest.TestCase):
    def test_pdd_skill_defines_scope_per_step_and_output(self):
        for tree in TREES:
            pdd = read(f"{tree}/skills/prompt-driven-development/SKILL.md")
            self.assertIn("## Test Scope and Output", pdd, tree)
            self.assertIn("| GREEN execution | The full suite once;", pdd, tree)
            self.assertIn("| Final Review | Rerun only when no full run is recorded", pdd, tree)
            self.assertIn("Never copy the full log into the conversation or an artifact.", pdd, tree)
            self.assertIn("Do not poll.", pdd, tree)
            self.assertIn("The gate still waits", pdd, tree)

    def test_execution_commands_scope_their_runs(self):
        expected = {
            "generate-tests": "Run only the new tests",
            "implement-approved-plan": "for GREEN, the full suite once",
            "refactor-code": "run the full suite once",
            "review-code": "Rerun the full verification only when no full run is recorded",
        }
        for op, phrase in expected.items():
            for rel in command_pair(op):
                self.assertIn(phrase, read(rel), rel)
        for op in ["generate-tests", "implement-approved-plan", "refactor-code"]:
            for rel in command_pair(op):
                self.assertIn("write output to a log file" if op != "implement-approved-plan" else "Write output to a log file", read(rel), rel)


class PairedPlanTest(unittest.TestCase):
    def test_paired_plan_is_the_one_exception(self):
        for tree in TREES:
            pdd = read(f"{tree}/skills/prompt-driven-development/SKILL.md")
            self.assertIn("A single Implementation Plan authorizes exactly one milestone", pdd, tree)
            self.assertIn("The one exception is a paired plan", pdd, tree)
            self.assertIn("**One pair, one plan (small changes).**", pdd, tree)
            self.assertIn("test files do not count", pdd, tree)
            self.assertIn("RED evidence is still required before any production change.", pdd, tree)
            self.assertIn("RED executed — see Plan.md; GREEN approved, not yet executed", pdd, tree)
            plan = read(f"{tree}/skills/prompt-driven-development/templates/Plan.md")
            self.assertIn("one pair, one plan", plan, tree)
        for rel in command_pair("generate-tests"):
            self.assertIn("For a paired plan, apply only its RED part.", read(rel), rel)
        for rel in command_pair("implement-approved-plan"):
            self.assertIn("the GREEN part of a paired plan whose RED part is recorded as executed", read(rel), rel)
        for rel in command_pair("create-implementation-plan"):
            self.assertIn("NNN_Implementation_Plan_<RED>_<GREEN>.md", read(rel), rel)


class InputsAndAnswersTest(unittest.TestCase):
    def test_fresh_context_input_table(self):
        for tree in TREES:
            pdd = read(f"{tree}/skills/prompt-driven-development/SKILL.md")
            self.assertIn("and only the inputs it needs:", pdd, tree)
            self.assertIn("| `generate-tests` (RED) | requirements, Plan, contract, its Implementation Plan, repository |", pdd, tree)
            self.assertIn("| `implement-approved-plan`, `refactor-code` | Plan (status and predecessor evidence), its Implementation Plan, repository |", pdd, tree)

    def test_execution_reads_no_requirements_or_contract(self):
        for op in ["implement-approved-plan", "refactor-code"]:
            for rel in command_pair(op):
                text = read(rel)
                self.assertNotIn("the authoritative requirements, Plan, and applicable API/external contract", text, rel)
                self.assertNotIn("- the authoritative artifacts;", text, rel)
        for rel in command_pair("generate-tests"):
            self.assertIn("the authoritative requirements, Plan, and applicable API/external contract", read(rel), rel)

    def test_planner_reads_earlier_plans_briefly(self):
        for rel in command_pair("create-implementation-plan"):
            self.assertIn("Review Summary and Carried-Forward Decisions, and its exact code only for files this milestone touches", read(rel), rel)

    def test_answers_are_recorded_in_the_artifact(self):
        for tree in TREES:
            pdd = read(f"{tree}/skills/prompt-driven-development/SKILL.md")
            self.assertIn("Answers to a command's questions are recorded in the artifact", pdd, tree)
            self.assertIn("The main conversation does not edit the artifact itself.", pdd, tree)
        for op in ["create-plan", "create-api-contract", "create-implementation-plan"]:
            for rel in command_pair(op):
                self.assertIn("record each in the", read(rel), rel)


if __name__ == "__main__":
    unittest.main()
