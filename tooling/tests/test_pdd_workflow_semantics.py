from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]

ACTIVE_GUIDANCE_PATHS = [
    ROOT / "README.md",
    ROOT / ".github",
    ROOT / "agents",
    ROOT / "playbooks",
    ROOT / "standards",
    ROOT / "stacks",
    ROOT / "examples",
    ROOT / "templates" / "docs",
]

# These phrases represent the obsolete PDD model in which a single milestone
# or Implementation Plan authorized RED, GREEN, and REFACTOR together.
OBSOLETE_PHRASES = (
    "RED, GREEN, and Refactor happen inside each implementation milestone",
    "RED, GREEN, and Refactor happen inside each milestone",
    "must not be separate milestones",
    "must not be modeled as delivery milestones",
    "milestones describe delivery outcomes, not RED/GREEN execution phases",
    "run RED → GREEN → REFACTOR from an approved implementation plan",
    "execute RED → GREEN → REFACTOR from an approved implementation plan",
)


def markdown_files():
    for target in ACTIVE_GUIDANCE_PATHS:
        if target.is_file():
            yield target
            continue
        if not target.exists():
            continue
        for path in target.rglob("*.md"):
            # Historical planning artifacts are evidence, not active guidance.
            if "docs/.ai" in path.as_posix():
                continue
            yield path


class PddWorkflowSemanticTests(unittest.TestCase):
    def test_active_guidance_does_not_reintroduce_collapsed_phase_model(self):
        failures = []
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in OBSOLETE_PHRASES:
                if phrase.lower() in lowered:
                    failures.append(f"{path.relative_to(ROOT)}: {phrase}")

        self.assertEqual([], failures, "Obsolete PDD phase semantics found:\n" + "\n".join(failures))

    def test_canonical_workflow_requires_separate_phase_milestones(self):
        workflow = (ROOT / "standards/prompt-driven-development-workflow.md").read_text(encoding="utf-8")
        self.assertIn("RED is a separate milestone", workflow)
        self.assertIn("GREEN is a separate milestone", workflow)
        self.assertIn("REFACTOR is a separate milestone when refactoring is justified", workflow)
        self.assertIn("Do not advance to the next phase milestone until its own Implementation Plan is approved", workflow)

    def test_red_execution_stops_before_green(self):
        prompt = (ROOT / ".github/prompts/generate-tests.prompt.md").read_text(encoding="utf-8")
        self.assertIn("Stop after valid RED", prompt)
        self.assertIn("Do not change production code, production configuration, or production contracts", prompt)

    def test_green_execution_stops_before_refactor(self):
        prompt = (ROOT / ".github/prompts/implement-approved-plan.prompt.md").read_text(encoding="utf-8")
        self.assertIn("Stop after GREEN", prompt)
        self.assertIn("Do not advance to another Plan milestone in this invocation", prompt)

    def test_refactor_requires_its_own_milestone(self):
        prompt = (ROOT / ".github/prompts/refactor-code.prompt.md").read_text(encoding="utf-8")
        self.assertIn("REFACTOR", prompt)
        self.assertIn("predecessor GREEN", prompt)
        self.assertIn("Do not combine feature behavior or defect fixes with refactoring", prompt)

    def test_implementation_plan_template_is_phase_specific(self):
        template = (ROOT / "templates/docs/implementation-plan-template.md").read_text(encoding="utf-8")
        self.assertIn("**Phase:** FOUNDATION | RED | GREEN | REFACTOR | OTHER", template)
        self.assertIn("Complete **only the section matching the milestone Phase**", template)
        self.assertIn("No production implementation changes", template)
        self.assertIn("No refactoring; use a separately approved REFACTOR milestone", template)


if __name__ == "__main__":
    unittest.main()
