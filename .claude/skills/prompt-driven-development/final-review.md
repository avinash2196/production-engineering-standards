# Prompt-Driven Development — Final Review Authority

Part of the `prompt-driven-development` skill (see its Parts table). Apply it together with the core `SKILL.md`.

## Final Review Authority

Final Review of a work item is performed only by `review-code` or `review-production-readiness`, when the user names the work item. Other reviews — for example `review-architecture` or `review-requirements` — are intermediate and do not close the work item. Any review produces findings and recommendations only; a finding is not an authorized change. Never apply one directly to code, tests, or configuration: a finding that needs an executable change goes through the normal chain — the authoritative artifact when scope changes, then a new or amended Implementation Plan (a fix work item, Fix Work Items), RED before GREEN when behavior or validation changes. There is no trivial-change exception for executable artifacts.

When a review is the Final Review of a Plan, write it to `docs/.ai/<work-item>/Final-Review.md` — the verdict, each Final Acceptance Criterion with its evidence, an answer to every Final Review obligation row in the Plan's traceability, the findings, and the recommendation — and add a Final Review row to `Plan.md` Execution Status pointing to it, with the status "Written — awaiting user decision" (never "Completed"). Change no other file. Accepting the findings is the user's decision, recorded by the user in that file. Final-Review.md also lists each product-level statement now out of date in `docs/requirements.md`, and each statement in user-facing documentation such as README files that the work item made false, for the user to update; the review does not edit them.

- Use `templates/Final-Review.md` for the structure, and mark each finding as pre-existing or introduced by the work item.
- Before raising a finding, read `Plan.md` Execution Status evidence and the approved Implementation Plans; drop any finding that recorded evidence or an approved decision contradicts.
- Never recommend reverting an approved decision as a fix; raise it as a question for the user.
- Give a severity only with a concrete failure scenario, and cite the correct path.
- A criterion that names a real external system and has only double evidence, with no accepted gap in the requirements or the Plan, is a blocking finding: the review cannot recommend acceptance until real evidence is added or the user accepts the gap.
- An error in an earlier approved artifact (for example a wrong explanation in an Implementation Plan) is recorded as a finding in Final-Review.md; do not edit the approved artifact.
