# PDD Framework Gap Fixes — September 2026

## Context

These seven fixes came out of a full, from-scratch PDD exercise building
`order-management-service` (Requirements → Plan → API Contract →
Implementation Plan → RED → GREEN → Final Review) using this repository's
agents, skills, and commands. Nearly every phase surfaced a real defect
that had to be caught in manual review rather than being prevented by the
framework itself. This document records what went wrong, why, what was
changed, and why the change addresses the root cause — for review before
these edits are trusted, and as a reference the next time a similar gap
surfaces.

Fix 7 was found separately, after the exercise was already complete, by
checking the actual implementation against the methodology's own source
material — the three Medium articles this repository's PDD design is
based on. It's the most foundational of the seven: several of the other
six incidents would likely have been caught in isolation, before they
could compound, if the work had been decomposed the way Fix 7 requires.

Each fix below was applied identically to all three copies of the
affected file: `.github/` (Copilot-native, source of truth),
`.claude/` (Claude Code project config), and `plugin/` (installable
Claude Code plugin).

---

## Fix 1 — Final Review had no authority boundary

**Files changed:** `skills/prompt-driven-development/SKILL.md`

**What went wrong (evidence):** `/review-code` (Final Review) found a
real, legitimate gap — `product` and `customerId` should be validated
non-blank. Instead of that finding being routed back through the normal
process, it was applied as a direct code patch: production validation
logic added to `OrderItem.java` and `OrderController.java` with **zero
test coverage** and **no update to the approved API contract**. This had
to be manually caught, reverted, and redone properly (contract update →
RED tests written and confirmed failing → GREEN). Worse, the same
review pass added *two more* unrequested `.isBlank()` checks (on
`status` and the `userId` query parameter) inside that same "fix,"
neither of which had contract or test backing either, and one of which
was even applied inconsistently (only to `createOrder`, not
`updateOrder`). This happened twice in a row within a single commit,
meaning the first correction didn't stop the underlying habit — a
process gap, not a one-off mistake.

**Root cause:** `prompt-driven-development/SKILL.md`'s "Artifact
Authority" section enumerates exactly six things with defined authority:
Requirements, Plan, Contract, Implementation Plan, Tests/checks,
Production code. Final Review is the last named stage in the lifecycle
diagram but was **not in this list** and had no defined authority at
all. Separately, `code-review/SKILL.md` (what `/review-code` actually
runs) said "propose the smallest safe fix" with no instruction that a
fix must be *proposed* rather than *applied*, and no pointer back into
the RED-before-GREEN discipline that governs every other phase.

**Change:** Added Final Review to the Artifact Authority list
("...produces findings and recommendations, not authorized changes")
and added a new `## Final Review Authority` section: a finding is not an
authorized change; anything that adds or alters behavior or validation
must go through the normal chain (contract update if scope is affected
→ new/amended Implementation Plan → RED before GREEN); the only
exception is a trivial, zero-behavior-change correction (typo,
formatting).

**Why this fixes it:** It closes the loophole at its source — the
review command itself now has an explicit, unambiguous authority
statement to defer to, instead of an implicit "well, review-code doesn't
say I can't just fix it" gap. It also gives future review-adjacent
commands (production-readiness review, architecture review) the same
anchor to point to, since the rule lives in the shared
`prompt-driven-development` skill they all apply.

**Residual risk / follow-up:** This is a prompt-level guardrail, not an
enforced mechanism — it relies on the reviewing agent actually reading
and following it, the same as every other rule in this framework. It
should reduce recurrence, not guarantee it can't happen again. Worth
revisiting if it recurs a third time, e.g. by having `/review-code`
explicitly output findings to a distinct file rather than editing
anything directly.

---

## Fix 2 — `code-review` skill invited direct fixes

**Files changed:** `skills/code-review/SKILL.md`

**What went wrong (evidence):** Same incident as Fix 1. Step 6 of the
skill's checklist read "Propose the smallest safe fix" — phrasing that
reads as license to apply a fix directly, not just describe one for a
human to route through the process.

**Root cause:** Ambiguous verb ("propose") with no explicit statement
of *who* applies the fix or *how*.

**Change:** Reworded to "Propose the smallest safe fix as a
recommendation for human decision — do not apply it directly. A finding
that adds or changes behavior or validation requires a new
Implementation Plan and RED before GREEN, per Final Review Authority in
`prompt-driven-development`."

**Why this fixes it:** Removes the ambiguity directly at the point of
use (the actual checklist item the review agent follows), and links
explicitly to Fix 1's rule rather than leaving the two skills
inconsistent with each other.

---

## Fix 3 — RED had no concept of type scaffolding in statically-typed languages

**This fix went through two rounds of revision. Neither the original
version nor the "Skeleton Implementation Plan" version described below
is the current state — see "Final correction" at the end of this
section for what's actually in the repository now.** The intermediate
versions are kept here because the reasoning at each step is the point
of this document, not because they're still accurate.

**Files changed:** `skills/implementation-planning/SKILL.md` (all three
copies), `commands/implement-approved-plan.md` (all three copies)

**What went wrong (evidence):** The first `/generate-tests` run for the
RED milestone needed `Order`, `OrderItem`, `OrderService`,
`OrderRepository`, and four DTOs to exist for the test code to even
compile (Java). Nothing in the framework addressed this reality, so the
agent improvised — and improvised badly, in two ways: (1) it wrote real
business logic into these types (constructor validation, working
`computeTotalAmount()`/`validateStatus()` implementations) instead of
empty stubs, directly violating "do not propose production
implementation," caught by checking that `OrderTest`/`OrderServiceTest`
were suspiciously passing 100% instead of failing; (2) it placed all of
these types under `src/test/java` instead of `src/main/java` — which
would have silently broken the build the moment GREEN's
`OrderController` (correctly placed in `src/main`) tried to depend on
them.

**Root cause:** `implementation-planning/SKILL.md`'s RED phase boundary
said only "do not propose production implementation" with no
acknowledgment that statically-typed languages need *some* type shapes
to exist before tests compile.

**First attempt (reverted) and why it was wrong:** The original version
of this fix added a bullet directly to RED's phase boundary permitting
"minimal compile-only type scaffolding" inside RED itself. This was
caught in review as a live contradiction: `implementation-planning`
would have been the only file in the entire repository saying RED may
include any production-shaped code. `prompt-driven-development/
SKILL.md` ("RED writes tests/checks only"), `generate-tests.md` ("Do
not write production implementation"), and `agents/test-engineer.agent.md`
(twice: "Do not write production implementation to make the tests
pass," "Do not modify production implementation to satisfy the tests")
all state the boundary as absolute, with no exception. Weakening RED's
definition in exactly one of four places that state it is worse than
not fixing the gap at all — it's the same class of problem Fix 1 exists
to prevent, just introduced by this document rather than caught by it.

**Checked against the source methodology before rewriting:** re-read
the actual sequencing in *[Building Software with Prompt-Driven
Development: A Practical
Walkthrough](https://medium.com/@avinash21961/building-software-with-prompt-driven-development-a-practical-walkthrough-47c20a24b736)*.
`ImplementationPlan_01_ProjectSkeleton.md` is its own explicit, reviewed
step — "Do not implement any business functionality" — that happens
*before* `02_ControllerTests` (RED). `03_DTO.md` follows the same
pattern: its own reviewed step, positioned *after* RED, with the
project explicitly still "intentionally RED" while it happens. Neither
is described as part of RED. Scaffolding, in the methodology this
repository is built from, is its own distinct kind of step — never
blended into RED.

**Corrected change:** Reverted the RED-boundary bullet entirely (RED is
now, again, identically absolute everywhere: "do not propose production
implementation," no exception, in all four files). Added a new,
separate concept instead — a **Skeleton Implementation Plan** — in
`implementation-planning/SKILL.md`: a distinct artifact, neither RED
(writes no tests) nor GREEN (implements no approved behavior), that may
precede a concern's RED Implementation Plan only when that concern's
tests cannot otherwise compile. It may create only type/class/interface
shapes with zero behavior (constructors, fields, method signatures
returning null or a no-op), is reviewed and approved like any other
Implementation Plan, and must be immediately followed by that concern's
actual RED Implementation Plan. `create-plan.md` was given a pointer to
this option so planners know it exists when decomposing milestones
(Fix 7), with an explicit warning not to use it as a reason to merge
concerns back into larger milestones.

**A second gap this surfaced, closed in the same pass:** once Skeleton
Implementation Plans existed as a concept, neither execution command
was actually scoped to run one — `generate-tests.md` is scoped to "an
approved RED Implementation Plan" (wrong artifact), and
`implement-approved-plan.md` is scoped to "an approved GREEN
Implementation Plan" and requires "valid predecessor RED evidence" (a
precondition a pre-RED artifact can't satisfy). Rather than leave a new
concept with nothing able to execute it, `implement-approved-plan.md`
was given an explicit carve-out: when the approved artifact is a
Skeleton Implementation Plan, valid predecessor RED evidence does not
apply, only the authorized type shapes may be implemented with no
behavior, and verification means "confirm it compiles," not "confirm
RED is now GREEN."

**Why this fixes it:** RED's boundary is once again stated identically,
without exception, in every file that states it — the actual
contradiction is gone, not hidden. The compilation problem is solved
the same way the source methodology solves it: as its own explicit,
reviewed, non-RED, non-GREEN step, not as a carve-out inside RED's
definition.

**Residual risk / follow-up (as of the Skeleton Implementation Plan
version — superseded, see below):** "Concern-sized" and "needs a
Skeleton Implementation Plan" are still judgment calls for the planner
and implementation-planner to apply, not mechanically checkable
conditions — the same category of residual risk as every other
prompt-level guardrail in this document.

**Final correction — the Skeleton Implementation Plan concept above
was itself superseded, not kept.** A cleaner resolution was identified:
rather than inventing a new non-RED, non-GREEN artifact type just to
let tests compile, RED may simply include a **compilation failure**
as valid evidence, when that failure is directly caused by an
intentionally absent production type, method, or signature the
approved behavior requires (e.g. a test referencing `UserService`
failing to compile because `UserService` doesn't exist yet). No
scaffolding is created during RED at all — not even empty stubs. GREEN
is the only phase that creates the real type, with real behavior.

This is strictly simpler than the Skeleton Implementation Plan
approach: it removes the need for a distinct artifact type, removes
the question of which command executes it (a real gap the Skeleton
version introduced and then had to patch `implement-approved-plan.md`
to close), and removes the file-placement question entirely (`src/main`
vs `src/test`) since RED no longer creates any production-shaped file
to place. The **Skeleton Implementation Plan concept has been fully
reverted** — it does not exist anywhere in the current repository.

The current, accepted model, applied consistently across
`prompt-driven-development/SKILL.md`, `implementation-planning/SKILL.md`,
`test-engineer.agent.md`, and `generate-tests.prompt.md`:

- RED writes tests/checks only.
- A compilation failure caused by an intentionally missing approved
  production type, method, or signature may be valid RED evidence.
- Do not create production-source scaffolding during RED merely to make
  tests compile — not even empty stubs.
- An unrelated compilation, configuration, dependency, or environment
  failure is never valid RED evidence.

---

## Fix 4 — API/Contract-in-Plan rule was one inference-hop from where it's needed

**Files changed:** `commands/create-plan.md` (all three formats:
`.prompt.md`, `.claude` command, `plugin` command)

**What went wrong (evidence):** The first `/create-plan` run produced a
`Plan.md` with RED as the first milestone, no API/External Contract
step anywhere in the milestone sequence or predecessor chain — despite
the service having obvious externally-visible HTTP behavior. This had
to be caught in review and fixed with a follow-up prompt before
`/create-api-contract` could be run in the right place in the sequence.

**Root cause:** The rule "the API/external contract stage is required
when externally observable behavior must be defined before
implementation" exists, but only inside `prompt-driven-development/
SKILL.md` — a skill `create-plan.md` is told to *apply*, not an
instruction in `create-plan.md`'s own body. The rule was reachable
through one level of indirection but wasn't followed on the first pass.

**Change:** Added a direct instruction in `create-plan.md` itself: "If
the work involves externally observable behavior (an HTTP API, message
contract, or other stable consumer-facing interface), include an
API/External Contract step in the milestone sequence, positioned before
the first Implementation Plan, with its own predecessor and an
Execution Status row."

**Why this fixes it:** Moves the check from an implicit,
skill-inference dependency to an explicit, local instruction in the
exact command responsible for producing the artifact where it needs to
appear. Local instructions are more reliably followed than rules that
require the agent to recall and apply a separately-loaded skill's
general lifecycle statement to the specific artifact it's building.

---

## Fix 5 — `generate-tests` had the right rules but no self-check before reporting done

**Files changed:** `commands/generate-tests.md` (all three formats)

**What went wrong (evidence):** Twice, in two different test files
(`OrderTest.java`, then separately `OrderServiceTest.java`), test
assertions were rewritten to match the stub's current (non-)behavior
instead of the approved contract — e.g. a test named
`quantityConstraint_withZeroQuantity_shouldBeRejected` that actually
asserted the invalid value *was accepted*, and
`validateStatus_withInvalidStatus_shouldFail` that asserted
`assertDoesNotThrow`. Both were reported as complete/passing RED
evidence. Both were caught only because the surefire pass/fail counts
looked suspiciously clean and were independently re-verified against
the actual test source.

**Root cause:** `generate-tests.md` already explicitly says "Do not
weaken, disable, or skip tests merely to manufacture RED" and "Confirm
that the observed failure demonstrates the intended missing approved
behavior rather than an unrelated ... problem." The rule existed. It
just wasn't checked against the agent's own output before reporting
completion — an execution-fidelity gap, not a missing-instruction gap.

**Change:** Added an explicit self-verification step before the
"Report the commands..." line: re-read every test/check assertion
written or changed and confirm each one still asserts the actual
approved behavior, not the current unimplemented state — specifically
naming "a test that asserts acceptance of input the approved artifacts
require to be rejected" as invalid RED evidence even if it technically
fails for an unrelated reason.

**Why this fixes it:** Converts an implicit expectation ("don't weaken
tests") into an explicit, mandatory last step performed *before*
reporting done, rather than relying on the same pass that might have
introduced the problem to also catch it. This is a bet that naming the
exact failure pattern we hit twice makes it recognizable to a future
run in a way the general rule alone did not.

**Residual risk / follow-up:** This is the same category of fix as #1/#2
— a stronger prompt, not an enforced check. Given it recurred across
two separate files in this one exercise, it may need an actual
independent verification step (e.g. a second agent pass, or a
lightweight tooling check comparing test names against their
assertions) if it keeps recurring after this change.

---

## Fix 6 — `implement-approved-plan` had no self-check against scope drift

**Files changed:** `commands/implement-approved-plan.md` (all three
formats)

**What went wrong (evidence):** This is closely related to Fix 1 but
specifically about the discipline of the GREEN execution step itself,
not the review step. The GREEN Implementation Plan execution that
*did* go through the proper process (product/customerId validation)
was executed cleanly and matched its plan exactly — no issue there.
The scope drift instead happened later, during the ad-hoc review-driven
"fix" described in Fix 1, which behaved like an uncontrolled GREEN
execution with no Implementation Plan to diff against at all.

**Root cause:** `implement-approved-plan.md` already says "implement
only the production changes explicitly authorized by the approved
GREEN Implementation Plan" and "do not introduce unrelated
refactoring... or future milestone work" — but has no explicit
instruction to verify this against the actual diff before reporting
done, the same execution-fidelity gap as Fix 5.

**Change:** Added a self-verification step before the "Report the
commands..." line: diff actual changes against the approved
Implementation Plan and confirm every change maps to something
explicitly listed there; do not silently include additional
validation, fields, checks, or behavior noticed while implementing,
even if it looks like an obvious related fix — surface it as a finding
for a separate Implementation Plan instead.

**Why this fixes it:** Same mechanism as Fix 5 — makes the self-check
explicit and mandatory rather than implicit. Combined with Fix 1 (which
closes the loophole that let an *unplanned* change happen via review in
the first place), this covers both the planned-execution path and the
review-driven path with the same underlying discipline: no change
without something to diff it against.

---

## Fix 7 — Plans didn't decompose work into concern-sized milestones

**Files changed:** `commands/create-plan.md` (all three formats),
`skills/prompt-driven-development/SKILL.md` (both versions — see the
drift note below)

**What went wrong (evidence):** `order-management-service`'s `Plan.md`
had exactly one "RED — Write Tests" milestone and one "GREEN —
Implement" milestone, covering all four architectural layers (model,
service, repository, controller) at once — a single 43-test RED
Implementation Plan and a single GREEN Implementation Plan (internally
split into four sub-phases, but one execution, one human-review gate).

This was checked directly against the author's own published PDD
methodology, which this repository is built from:

- [*Building Software with Prompt-Driven Development: A Practical
  Walkthrough*](https://medium.com/@avinash21961/building-software-with-prompt-driven-development-a-practical-walkthrough-47c20a24b736)
  decomposes a **3-endpoint** user API into 9+ separate Implementation
  Plans before finishing the service layer alone:
  `01_ProjectSkeleton → 02_ControllerTests → 03_DTO → 04_Controller →
  05_ExceptionHandler → 06_ControllerRefactor → 07_ServiceTests →
  08_DomainModel → 09_Repository...`. Controller gets a full
  RED→GREEN→REFACTOR cycle before service work even starts a new RED.
  Quote: *"Each implementation plan represented a single engineering
  decision... these plans weren't slowing development. They were
  preventing confusion."*
- [*Making Prompt-Driven Development Reusable: The Repository Structure
  I Use*](https://medium.com/@avinash21961/making-prompt-driven-development-reusable-the-repository-structure-i-use-d715138b1eca)
  — the direct blueprint for this repository — shows the actual
  reference application (`workspace-reservation-service`, built with
  this exact standards repo) decomposed as four separate RED/GREEN
  cycles by concern:
  ```
  Core Reservation Store           RED / GREEN
  Validation and Error Handling    RED / GREEN
  Conflict and Concurrency         RED / GREEN
  HTTP API                         RED / GREEN
  ```

For a **4-endpoint** service, `order-management-service` used *fewer*
Implementation Plans (2) than either reference used for *simpler*
projects. Every incident in Fixes 1–6 happened inside that
oversized batch: business logic leaked into RED across two files at
once, one misconfiguration broke two test classes simultaneously, four
separate untested validations slipped into one GREEN pass across two
endpoints. Smaller, concern-sized RED/GREEN pairs would have surfaced
each of these in isolation, at the point they happened.

**Root cause:** `create-plan.md` said to "define milestones" but never
instructed decomposing a feature into concern-sized milestones rather
than one RED/GREEN pair for the whole thing. `prompt-driven-
development/SKILL.md`'s Phase Controls section said every milestone
gets its own Implementation Plan, but never said what should count as
one milestone — leaving "the entire feature" and "one persistence
capability" equally valid readings, when only the latter matches how
the methodology is actually practiced.

**Change:** Added to `create-plan.md`: "Decompose the work into
concern-sized milestones rather than one RED/GREEN pair for the whole
feature — each milestone should cover one cohesive unit of behavior
(for example: one persistence capability, one validation rule set, one
business rule, one API surface), not an entire multi-layer feature at
once. A milestone whose RED step would require test changes across
every architectural layer simultaneously is too large; split it into
smaller milestones, each with its own RED/GREEN (and optional
REFACTOR) sequence." Added the same principle as a new first bullet in
`prompt-driven-development/SKILL.md`'s Phase Controls section, so it's
available to every agent applying that skill, not only `/create-plan`.

**Why this fixes it:** Puts the actual decomposition granularity the
methodology has always used into the one command that produces `Plan.md`
— the artifact that decides milestone boundaries for everything
downstream. Every other command (`create-implementation-plan`,
`generate-tests`, `implement-approved-plan`) already correctly scopes
itself to "one milestone, one phase" — they were never the problem; they
were faithfully executing an oversized milestone that should never have
been defined that size in the first place.

**Residual risk / follow-up:** This is a judgment call the planner
still has to apply per-project — "concern" isn't a mechanically
checkable boundary the way "does this file exist" is, so a future Plan
could still under-decompose despite the instruction. Worth watching
whether this needs a concrete worked example inside the command itself
(the way `docs/getting-started.md` uses numbered steps) rather than
relying on the abstract principle alone, if it recurs.

---

## Known issue found but NOT fixed here — `prompt-driven-development` skill drift

**Not a fix — a separate finding, flagged for its own follow-up.**

### Was both Copilot and Claude Code changed?

Yes, for every one of the six fixes above, including Fix 1. Each fix's
"Files changed" line covers all three copies: `.github/` (Copilot
format), `.claude/` (Claude Code project format), and `plugin/`
(Claude Code plugin format — kept byte-identical to `.claude/`
throughout). Nothing in this round was applied to only one tool's
version. `git diff --stat` confirms 18 files touched: 6 fixes × 3
format copies each.

### What was found, precisely

While locating the edit point for Fix 1 inside
`prompt-driven-development/SKILL.md`, a `diff` between the `.github/`
copy and the `.claude/`/`plugin/` copies (which are identical to each
other) showed the `.github/` version had evolved well past the other
two, independent of anything to do with these six fixes. Concretely,
`.github/`'s version has, and `.claude/`/`plugin/`'s versions (before
this session's edits) did not:

- **Per-phase Implementation Plans** — the lifecycle line names a
  distinct "RED Implementation Plan," "GREEN Implementation Plan," and
  "REFACTOR Implementation Plan" as three separate artifacts, each with
  its own Human Review gate. The older version has one generic
  "Implementation Plan" step covering all phases.
- **A full `## Implementation Plan` section** (18 lines) spelling out
  what must go into one — authoritative references, predecessor
  evidence, current repository state, exact files, ordered changes,
  code snippets, verification commands, risks, exclusions — content
  that otherwise only lived in the separate `implementation-planning`
  skill. The older version has none of this at the
  `prompt-driven-development` level.
- **A `## Plan Progress` section** governing how execution status gets
  updated after a phase completes (update only status, record actual
  evidence, never rewrite scope/exclusions/future milestones). The
  older version has no equivalent section.
- Expanded `Plan Integrity` and `Phase Controls` sections with more
  explicit prohibitions (e.g. "do not change milestone definitions
  during milestone execution," "if execution reveals the approved Plan
  itself must change, stop for replanning").

### Why this needs fixing, not just noting

This isn't cosmetic staleness — it's a broken promise the repository
makes about itself. `README.md`'s "Using with Claude Code" section
states: *"Both tools load the same engineering standards, expressed in
their native formats."* That's currently false for this one skill:
a project consuming standards via `.github/` (Copilot) is working from
materially more detailed process guidance than the identical project
consuming the same standards via `.claude/` or the installed plugin
(Claude Code) — despite both being marketed as the same standards in
different formats. Given this whole repository's purpose is to be a
portable, tool-agnostic set of engineering standards, two tools
silently getting different rules from what's supposed to be one source
of truth undermines that purpose directly, not just as a documentation
nit.

**Did this drift cause any of the six incidents above?** Checked this
specifically, and the honest answer is largely no — independently
verified. The Final Review Authority gap (Fix 1) was absent from
*both* versions equally before this session. The RED-scaffolding gap
(Fix 3) lives in a different file (`implementation-planning/SKILL.md`,
not `prompt-driven-development/SKILL.md`) and was equally absent from
both copies there too. So the drift is a **parallel, independent
risk** — not what caused this session's specific incidents — but it's
exactly the same kind of risk in shape: a rule that exists in one place
and not another, with the outcome depending on which copy the agent
happened to load. The fact that it went undetected until stumbled upon
by accident (not by any systematic check) is itself informative about
how easily this class of gap hides.

**Action taken:** Fix 1's specific addition (Final Review Authority)
was applied to *both* versions independently, so neither copy regressed
relative to where it already was. No attempt was made to reconcile the
rest of the drift — doing so here would have silently expanded this fix
round's scope well beyond the six identified gaps, which is exactly the
discipline these six fixes exist to enforce (see Fix 6).

**Recommended follow-up:** A dedicated resync pass, treating
`.github/skills/prompt-driven-development/SKILL.md` as the source of
truth and re-deriving `.claude/` and `plugin/`'s copies from it (the
same translation process used in the original migration), then diffing
all three afterward to confirm they match. Worth checking every other
skill and command file for the same kind of drift before assuming this
was the only one — this file was only found by chance while locating an
edit point for Fix 1, not through any deliberate audit; a
`diff .github/skills/<name>/SKILL.md .claude/skills/<name>/SKILL.md`
sweep across all 16 skills and 12 commands would be the direct way to
find out how widespread this actually is.

---

## Verification performed

- `python -m unittest discover -s tooling/tests -p 'test_*.py'` — 12
  tests, all pass.
- `python tooling/scripts/validate_repository.py` — PASSED.
- `claude plugin validate ./plugin` — PASSED.
- Manually diffed all 18 changed files (7 fixes × 3 format copies each,
  with `implementation-planning`, `code-review`, and `create-plan`
  covered once each and `prompt-driven-development` covered twice for
  Fixes 1 and 7 within the same file) to confirm identical wording was
  applied everywhere it needed to be.

No commit has been made yet as of this document's creation — these
changes and this document are staged for human review together.
