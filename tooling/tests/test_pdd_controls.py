import importlib.util
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

_SCRIPT_PATH = ROOT / "tooling" / "scripts" / "validate_repository.py"
_spec = importlib.util.spec_from_file_location("validate_repository", _SCRIPT_PATH)
validate_repository_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_repository_module)


class PddControlsTest(unittest.TestCase):
    def test_required_pdd_prompts_exist(self):
        required = [
            "capture-requirements.prompt.md",
            "create-plan.prompt.md",
            "create-api-contract.prompt.md",
            "create-implementation-plan.prompt.md",
            "generate-tests.prompt.md",
            "implement-approved-plan.prompt.md",
            "refactor-code.prompt.md",
            "review-code.prompt.md",
        ]
        for name in required:
            self.assertTrue((ROOT / ".github/prompts" / name).is_file(), name)

    def test_pdd_skill_preserves_authorization_boundaries(self):
        raw = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")
        # Normalize spacing around "/" so "API / External Contract" and
        # "API/External Contract" both satisfy the same token check.
        text = re.sub(r"\s*/\s*", "/", raw)

        for token in [
            "Requirements",
            "Plan",
            "API/External Contract",
            "RED",
            "GREEN",
            "REFACTOR",
            "Human Review",
            "Artifact Authority",
        ]:
            self.assertIn(token, text)

        self.assertIn("separate authorization boundaries", text)

    def test_pdd_skill_has_adaptive_milestone_decomposition(self):
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Adaptive Milestone Decomposition", text)
        self.assertIn("one pair per class or file", text)

    def test_pdd_skill_expresses_layer_wise_decomposition_for_complex_work(self):
        # Deterministic presence checks for the concepts this clarification
        # is about — not brittle wording, so unrelated future rewording of
        # the surrounding prose won't break this. Deliberately does not
        # assert on the illustrative Milestone 1/2/3/4 example text in
        # getting-started.md, only on the skill's own rule statements.
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")

        # complex requirements decompose into independently reviewable milestones
        self.assertIn("independently reviewable implementation milestones", text)
        # layer-wise decomposition is the expected pattern for complex layered work
        self.assertIn("layer-wise implementation milestones", text)
        self.assertIn("independently testable architectural layers", text)
        # a layer contributes separate RED/GREEN milestones, not one
        # containing milestone that owns them as internal phases
        self.assertIn(
            "There is no containing \"capability milestone\" that owns "
            "these as internal phases",
            text,
        )
        # layering is not a mandatory template
        self.assertIn("not a mandatory architectural template", text)

    def test_pdd_skill_defines_conditional_setup_foundation(self):
        # Deterministic presence checks for the conditional-SETUP concepts —
        # not brittle wording. This is deliberately narrow: it protects the
        # core invariants (conditional not mandatory; missing production
        # symbols are not a setup trigger; setup still requires an approved
        # Implementation Plan), not the exact prose.
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Conditional SETUP / FOUNDATION", text)
        # setup is conditional, not a default/mandatory milestone
        self.assertIn("never a default or mandatory milestone", text)
        # a missing production symbol alone is not a setup trigger — it's
        # still valid RED evidence, per the existing compile-failure rule
        self.assertIn("do not, by themselves, require SETUP", text)
        # setup still requires its own approved Implementation Plan, same as
        # RED/GREEN/REFACTOR — this is what prevents setup becoming a bypass
        self.assertIn(
            "requires its own approved SETUP/FOUNDATION Implementation Plan",
            text,
        )

    # --- Stabilization pass: FOUNDATION formally supported as a fourth
    # executable phase, alongside RED/GREEN/REFACTOR. Each test below
    # targets exactly one of the four conflicts this pass resolved.

    def test_foundation_is_a_recognized_executable_milestone_type(self):
        # Conflict 1: the authorization-defining sentence used to enumerate
        # only (RED, GREEN, or REFACTOR), contradicting the conditional-setup
        # rule elsewhere in the same document. FOUNDATION, RED, GREEN, and
        # REFACTOR are each their own milestone (not phases of a containing
        # milestone), and a single Implementation Plan authorizes exactly
        # one of them.
        skill_text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "FOUNDATION, RED, GREEN, and REFACTOR are each their own milestone",
            skill_text,
        )
        self.assertIn(
            "A single Implementation Plan authorizes exactly one milestone",
            skill_text,
        )

        planning_text = (
            ROOT / ".github/skills/implementation-planning/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("### FOUNDATION (conditional)", planning_text)

    def test_red_green_refactor_semantics_unchanged(self):
        # Conflict 1 must add FOUNDATION without weakening the existing
        # phase semantics — spot-check the load-bearing phrases survived.
        text = (
            ROOT / ".github/skills/implementation-planning/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("propose test/check changes only", text)
        self.assertIn(
            "require valid predecessor RED evidence when the PDD workflow applies",
            text,
        )
        self.assertIn("require a verified GREEN baseline", text)
        self.assertIn(
            "Do not create production-source scaffolding merely to make RED tests compile",
            text,
        )

    def test_foundation_remains_conditional_not_mandatory(self):
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("FOUNDATION is conditional", text)
        self.assertIn("most sequences proceed directly to a RED milestone", text)

    def test_missing_production_class_alone_does_not_require_foundation(self):
        planning_text = (
            ROOT / ".github/skills/implementation-planning/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "not merely because the production class, service, repository, "
            "controller, method, or behavior under test does not yet exist",
            planning_text,
        )

        prompt_text = (
            ROOT / ".github/prompts/create-implementation-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "the only reason under consideration is that the production "
            "class, service, repository, controller, method, or behavior "
            "under test does not yet exist",
            prompt_text,
        )

    def test_foundation_cannot_implement_target_feature_behavior(self):
        planning_text = (
            ROOT / ".github/skills/implementation-planning/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("explicitly exclude the target feature/business behavior", planning_text)

        exec_text = (
            ROOT / ".github/prompts/implement-approved-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "do not implement target feature/business behavior", exec_text
        )
        self.assertIn(
            "do not create speculative production scaffolding", exec_text
        )

    def test_implement_approved_plan_branches_foundation_and_green_explicitly(self):
        text = (
            ROOT / ".github/prompts/implement-approved-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn("If the approved Implementation Plan is FOUNDATION:", text)
        self.assertIn("If the approved Implementation Plan is GREEN", text)
        self.assertIn("A FOUNDATION execution never flows automatically into RED", text)

    def test_final_review_has_no_trivial_executable_code_exception(self):
        # Conflict 2: Final Review previously carved out a trivial
        # typo/formatting exception to the no-bypass rule — removed.
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("only exception is a trivial", text.lower())
        self.assertIn("There is no trivial-change exception for executable artifacts", text)

    # --- Final stabilization pass: planning-vs-execution responsibility,
    # new-vs-existing repository handling, and Acceptance/Completion
    # Criteria as their own explicit concept.

    def test_same_workflow_applies_to_new_and_existing_repositories(self):
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Apply this same current-state-driven decision to both new "
            "and existing repositories",
            text,
        )
        self.assertIn("Do not assume a new project automatically requires FOUNDATION", text)
        self.assertIn(
            "Do not assume an existing project automatically has every prerequisite",
            text,
        )

    def test_planning_not_execution_selects_foundation(self):
        # Planner/Plan.md decides whether a FOUNDATION milestone exists in
        # the sequence; the Implementation Planner and executor only read
        # and validate that decision (via the milestone type Plan.md
        # already recorded), never make it themselves.
        planning_text = (
            ROOT / ".github/skills/implementation-planning/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "it does not decide or change the milestone type", planning_text
        )
        self.assertIn(
            "Create a FOUNDATION Implementation Plan only when the "
            "milestone approved for this Implementation Plan is itself a "
            "FOUNDATION milestone, as recorded in `Plan.md`",
            planning_text,
        )

        prompt_text = (
            ROOT / ".github/prompts/create-implementation-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "it does not decide or change the milestone type", prompt_text
        )

        plan_template_text = (
            ROOT / ".github/skills/prompt-driven-development/templates/Plan.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "There is no containing milestone that owns several of these "
            "as internal phases",
            plan_template_text,
        )

    def test_executor_reads_milestone_type_and_does_not_decide_it(self):
        text = (
            ROOT / ".github/prompts/implement-approved-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "First read which milestone type the approved Implementation "
            "Plan declares",
            text,
        )
        self.assertIn("Do not decide the milestone type yourself", text)
        self.assertIn("Do not decide whether FOUNDATION is required", text)

    def test_executor_stops_on_unapproved_prerequisite_or_unmet_criteria(self):
        text = (
            ROOT / ".github/prompts/implement-approved-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "discovering during execution that an additional, unapproved "
            "prerequisite",
            text,
        )
        self.assertIn("do not add it automatically", text)
        self.assertIn(
            "discovering that an approved Acceptance/Completion Criterion "
            "cannot be satisfied",
            text,
        )
        self.assertIn(
            "do not change the criterion or broaden the implementation",
            text,
        )

    def test_acceptance_completion_criteria_required_and_distinct_from_verification(self):
        planning_text = (
            ROOT / ".github/skills/implementation-planning/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("explicit Acceptance / Completion Criteria", planning_text)
        self.assertIn(
            "Acceptance / Completion Criteria and verification are distinct",
            planning_text,
        )
        self.assertIn(
            "Do not invent or modify Acceptance / Completion Criteria during execution",
            planning_text,
        )

    def test_plan_milestone_is_a_single_execution_boundary_not_a_lifecycle_container(self):
        # Reversed from an earlier pass: a milestone is FOUNDATION, RED,
        # GREEN, or REFACTOR itself — not a capability/layer container that
        # owns a lifecycle of those as internal phases.
        text = (
            ROOT / ".github/skills/prompt-driven-development/templates/Plan.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "A milestone represents one independently approved execution "
            "boundary",
            text,
        )
        self.assertIn(
            "There is no containing milestone that owns several of these "
            "as internal phases",
            text,
        )
        self.assertIn("milestone type: FOUNDATION | RED | GREEN | REFACTOR | OTHER", text)
        self.assertNotIn("lifecycle:", text)
        self.assertNotIn("setup required:", text)

    def test_application_instructions_prefer_layers_without_forcing_them(self):
        # Conflict 3: "do not default... per architectural layer" could be
        # misread as opposing layer-wise decomposition. Both principles must
        # now coexist explicitly: no mechanical forcing, but prefer layering
        # for genuinely complex layered work.
        for rel in [
            ".github/skills/prompt-driven-development/templates/application-copilot-instructions.md",
            ".github/skills/prompt-driven-development/templates/application-claude-instructions.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(
                "Do not mechanically create one milestone per class",
                text,
            )
            self.assertIn(
                "create a separate RED milestone and GREEN milestone for "
                "each layer",
                text,
            )

    def test_plan_execution_status_is_milestone_based(self):
        # Reversed from an earlier pass that removed OTHER as a milestone
        # classification: OTHER is restored (milestone type is a
        # classification field, not an executable-workflow enum), and
        # Execution Status tracks milestones directly, never a nested
        # phase-status field.
        text = (
            ROOT / ".github/skills/prompt-driven-development/templates/Plan.md"
        ).read_text(encoding="utf-8")
        self.assertIn("OTHER", text)
        self.assertIn("| Milestone | Status | Evidence / Notes |", text)
        self.assertNotIn("phase-status", text.lower())

    def test_adaptive_decomposition_not_duplicated_as_exhaustive_list(self):
        # The full boundary catalog (persistence/domain/service/controller/
        # validation/concurrency/...) belongs only in getting-started.md as
        # illustrative documentation — runtime prompts should reference the
        # skill's rule, not redefine an exhaustive list of their own.
        exhaustive_markers = ["concurrency,", "migration,", "infrastructure/configuration"]
        runtime_files = [
            ".github/prompts/create-plan.prompt.md",
            ".claude/commands/create-plan.md",
            "plugin/commands/create-plan.md",
            ".github/agents/planner.agent.md",
            ".claude/agents/planner.md",
            "plugin/agents/planner.md",
            ".github/skills/prompt-driven-development/templates/Plan.md",
        ]
        for rel in runtime_files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            found = [m for m in exhaustive_markers if m in text]
            self.assertEqual(
                found,
                [],
                f"{rel} still duplicates the exhaustive boundary list: {found}",
            )

    def test_pdd_skill_forbids_red_production_scaffolding(self):
        skill_texts = "\n".join(
            (ROOT / rel).read_text(encoding="utf-8")
            for rel in [
                ".github/skills/prompt-driven-development/SKILL.md",
                ".github/skills/implementation-planning/SKILL.md",
                ".github/agents/test-engineer.agent.md",
                ".github/prompts/generate-tests.prompt.md",
            ]
        )

        self.assertIn("do not propose production implementation", skill_texts.lower())
        self.assertIn("scaffolding", skill_texts.lower())
        self.assertNotIn("Skeleton Implementation Plan", skill_texts)

    def test_pdd_skill_copies_are_synchronized(self):
        canonical_root = ROOT / ".github/skills"
        mirror_roots = [ROOT / ".claude/skills", ROOT / "plugin/skills"]

        for canonical_file in canonical_root.rglob("*"):
            if not canonical_file.is_file():
                continue
            rel = canonical_file.relative_to(canonical_root)
            canonical_text = canonical_file.read_text(encoding="utf-8")

            for mirror_root in mirror_roots:
                mirror_file = mirror_root / rel
                self.assertTrue(mirror_file.is_file(), f"missing {mirror_file}")
                self.assertEqual(
                    canonical_text,
                    mirror_file.read_text(encoding="utf-8"),
                    f"{mirror_file} has diverged from {canonical_file}",
                )

    def test_no_code_change_bypass_control_blocks_match_canonical(self):
        # This is the global control that closes the free-form-prompt
        # bypass: a real incident applied unreviewed code changes via a
        # prompt that never invoked any named PDD command, so this must
        # live in the always-loaded instruction files, not only inside
        # command prompts. Compared as a canonical block (single source of
        # truth in the validator module), not loose keywords — keyword
        # presence can pass even if a file asserts the opposite of the rule.
        m = validate_repository_module
        canonical = m._normalize_control_block(m.CANONICAL_NO_CODE_CHANGE_BLOCK)

        for rel in m.NO_CODE_CHANGE_REQUIRED_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            block = m._extract_control_block(text, m.NO_CODE_CHANGE_CONTROL_ID)
            self.assertIsNotNone(block, f"{rel}: missing PDD-CONTROL block")
            self.assertEqual(
                m._normalize_control_block(block),
                canonical,
                f"{rel}: PDD-CONTROL block diverges from the canonical rule",
            )

    def test_requirements_skill_has_blocking_clarification_gate(self):
        text = (
            ROOT / ".github/skills/requirements-analysis/SKILL.md"
        ).read_text(encoding="utf-8").lower()

        for token in [
            "material unresolved",
            "clarification",
            "stop",
            "wait",
        ]:
            self.assertIn(token, text)

    # --- Propagation pass: implementation-engineer aligned with FOUNDATION +
    # GREEN, the Implementation Plan template gains Acceptance/Completion
    # Criteria, lifecycle docs propagate conditional FOUNDATION, and every
    # phase executor verifies approved acceptance criteria before completion.

    def test_implementation_engineer_supports_foundation_and_green(self):
        text = (
            ROOT / ".github/agents/implementation-engineer.agent.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Execute an approved FOUNDATION or GREEN milestone's "
            "Implementation Plan",
            text,
        )
        self.assertIn("## FOUNDATION Branch", text)
        self.assertIn("## GREEN Branch", text)

    def test_implementation_engineer_does_not_decide_the_phase(self):
        text = (
            ROOT / ".github/agents/implementation-engineer.agent.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "was already selected by planning in `Plan.md` and fixed by "
            "the approved Implementation Plan — do not determine or "
            "change it",
            text,
        )
        self.assertIn("Do not add prerequisites, expand scope, or redesign", text)
        self.assertIn(
            "stop and return the issue to planning rather than performing it",
            text,
        )

    def test_implementation_plan_template_has_acceptance_completion_criteria(self):
        text = (
            ROOT
            / ".github/skills/prompt-driven-development/templates/Implementation-Plan.md"
        ).read_text(encoding="utf-8")
        self.assertIn("## Acceptance / Completion Criteria", text)
        self.assertIn(
            "State exactly what must be true for this specific milestone "
            "to be considered complete.",
            text,
        )
        # Distinct from, and ordered before, Verification/Expected Evidence.
        criteria_pos = text.index("## Acceptance / Completion Criteria")
        verification_pos = text.index("## Verification")
        evidence_pos = text.index("### Expected Evidence")
        self.assertLess(criteria_pos, verification_pos)
        self.assertLess(verification_pos, evidence_pos)

    def test_application_lifecycle_descriptions_include_conditional_foundation(self):
        # The two live application templates and README.md all use the
        # corrected milestone-per-type diagram.
        for rel in [
            ".github/skills/prompt-driven-development/templates/application-copilot-instructions.md",
            ".github/skills/prompt-driven-development/templates/application-claude-instructions.md",
            "README.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(
                "optional FOUNDATION milestone: Implementation Plan → "
                "Human Review → execution → Verification",
                text,
            )

    def test_getting_started_has_conditional_foundation_before_red(self):
        # Reversed from an earlier pass: FOUNDATION is its own milestone
        # with its own flow section, documented before the RED milestone's
        # flow section, not a conditional sub-branch of one milestone's
        # lifecycle.
        text = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8")
        self.assertIn(
            "For a FOUNDATION milestone (only when `Plan.md` records one "
            "as genuinely required):",
            text,
        )
        self.assertIn("For a RED milestone:", text)
        foundation_pos = text.index("For a FOUNDATION milestone (only when")
        red_pos = text.index("`/create-implementation-plan` for the RED milestone.")
        self.assertLess(foundation_pos, red_pos)

    def test_application_templates_describe_implementation_plan_as_milestone_specific(self):
        # Reversed from an earlier pass: FOUNDATION/RED/GREEN/REFACTOR are
        # each their own milestone, not phases within a containing
        # milestone, so an Implementation Plan authorizes one milestone —
        # not "one phase of one milestone."
        for rel in [
            ".github/skills/prompt-driven-development/templates/application-copilot-instructions.md",
            ".github/skills/prompt-driven-development/templates/application-claude-instructions.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(
                "Each Implementation Plan defines HOW one approved "
                "milestone will change the repository.",
                text,
            )
            self.assertNotIn(
                "Each Implementation Plan defines HOW one approved phase "
                "of one milestone will change the repository.",
                text,
            )

    def test_foundation_executor_verifies_acceptance_criteria(self):
        text = (
            ROOT / ".github/prompts/implement-approved-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "verify every approved FOUNDATION Acceptance / Completion "
            "Criterion",
            text,
        )

    def test_red_executor_verifies_acceptance_criteria(self):
        text = (
            ROOT / ".github/prompts/generate-tests.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "verify every approved RED Acceptance / Completion Criterion",
            text,
        )
        self.assertIn(
            "stop and report it to planning rather than changing the criterion",
            text,
        )

    def test_green_executor_verifies_acceptance_criteria(self):
        text = (
            ROOT / ".github/prompts/implement-approved-plan.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "verify every approved GREEN Acceptance / Completion Criterion",
            text,
        )

    def test_refactor_executor_verifies_acceptance_criteria(self):
        text = (
            ROOT / ".github/prompts/refactor-code.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "verify every approved REFACTOR Acceptance / Completion "
            "Criterion",
            text,
        )
        self.assertIn("existing GREEN baseline remains passing", text)

    def test_executors_stop_rather_than_reinterpret_criteria(self):
        # None of the four phase executors may invent, weaken, or modify
        # an approved Acceptance/Completion Criterion during execution.
        for rel in [
            ".github/prompts/implement-approved-plan.prompt.md",
            ".github/prompts/generate-tests.prompt.md",
            ".github/prompts/refactor-code.prompt.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(
                "do not invent, weaken, reinterpret, or modify",
                text,
            )

    def test_historical_doc_no_longer_presents_trivial_exception_as_current(self):
        text = (
            ROOT / "docs/pdd-gap-fixes-2026-09.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Later correction: this executable-code exception was removed.",
            text,
        )
        self.assertIn(
            "Current status: resolved in subsequent hardening; skill "
            "synchronization is now validator-enforced.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
