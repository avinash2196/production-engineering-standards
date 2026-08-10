# Plan: <Feature or Change Name>

**Date:** YYYY-MM-DD  
**Source:** <requirement, issue, or user request>  
**Status:** Draft | Approved | Superseded

## Objective

<What outcome is required and why?>

## Current State

- <Relevant existing behavior, files, or constraints>

## Scope

### In Scope

- <Required outcome>

### Out of Scope

- <Explicitly excluded work>

## Requirements and Constraints

- <Functional requirement>
- <Validation or business rule>
- <Architecture, security, compliance, or operational constraint explicitly supported by the input/current repository>

## Milestones

PDD milestones are intentionally small human-controlled execution boundaries.

For behavior-changing work, use separate milestones for:

- **RED** — tests/checks only; prove the approved behavior is missing.
- **GREEN** — minimum production implementation; requires valid predecessor RED evidence.
- **REFACTOR** — optional; separate milestone only when justified and must preserve GREEN behavior.

Do not combine RED, GREEN, and REFACTOR authorization into one milestone. Do not create empty phase milestones merely for ceremony.

A project/test foundation or another non-behavior artifact may be its own milestone when it is a real deliverable.

Keep every milestone small and independently reviewable. Do not pull later behavior, dependencies, configuration, abstractions, tests, or infrastructure into an earlier milestone merely to prepare for future work.

1. **<Milestone name>**
   - Phase: FOUNDATION | RED | GREEN | REFACTOR | OTHER
   - Outcome: <observable outcome required from this milestone only>
   - Depends on: <prior milestone or none>

2. **<Milestone name>**
   - Phase: FOUNDATION | RED | GREEN | REFACTOR | OTHER
   - Outcome: <observable outcome required from this milestone only>
   - Depends on: <prior milestone>

## Dependencies and Risks

- <Dependency or risk and how it affects sequencing>

## Success Criteria

- [ ] <Observable completion condition>
- [ ] <Required validation or test condition>

## Review Record

- Reviewer: <name or role>
- Decision: Pending | Approved | Changes Requested
- Notes: <review feedback>
