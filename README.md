enterprise-ai-engineering
=========================

Purpose
- Canonical repository of standards, templates, agents, and workflows that teams and Copilot-style agents use to produce production-ready backend services (Java Spring Boot and Python FastAPI).

System philosophy
- Configuration-first: runtime behavior is driven by typed configuration (operator overrides → dynamic config → env → local files → build defaults). All services must use the `ConfigProvider` pattern.
- Explicit fallbacks: every external dependency must provide an explicit, environment-controlled fallback (e.g., Kafka → file-queue, Redis → in-memory). Fallbacks are only for local/dev and must not silently weaken production guarantees.
- Capability abstractions: depend on small, well-documented interfaces (MessagePublisher, CacheProvider, ObjectStorageProvider, SecretProvider) so implementations are pluggable and testable.

Top-level structure (high level)
- `core/` — architecture, abstraction contracts, configuration and fallback strategy.
- `standards/` — mandatory engineering controls: security, observability, testing, compliance, performance.
- `stacks/` — opinionated language stacks and project templates (Java Spring Boot and Python FastAPI).
- `agents/` — Copilot-style agent specs and prompts (scaffolders, reviewers, compliance agents).
- `workflows/` — step-by-step developer and operational workflows (create service, add endpoint, prepare for production).
- `templates/` — ADRs, infra, monitoring, and repo-level templates.
- `examples/` — minimal runnable examples and fallback demos.
- `tooling/` — repo validators and generators.

Java + Python usage
- Java (Spring Boot): follow layered layout `controller → service → domain → repository`; use `@ConfigurationProperties` bound to `ConfigProvider`, `@ControllerAdvice` for errors, and Testcontainers for integration tests (or local fallbacks in CI).
- Python (FastAPI): use Pydantic models for DTOs, dependency injection via `Depends` for providers, async-safe handlers, and Testcontainers or local fallback adapters for integration tests.

How agents work
- Agents are first-class: they read `standards/` and `core/` and produce scaffolds, PR suggestions, or review reports. Key agents include `backend-service-builder`, `code-reviewer`, and `compliance-reviewer`.
- Agents may generate files and suggested patches; human review is required for commits. Agents are forbidden from committing secrets or running external network commands without explicit approval.

Fallback behavior
- Fallbacks are explicit, toggled by environment variables (e.g., `FALLBACK_KAFKA=true`).
- Fallbacks must emit telemetry (`fallback.active{name="<dep>"}`) and structured warnings when active.
- Behavior differences (durability, ordering, consistency) must be documented in the integration guide for each adapter.

Compliance
- This repo provides engineering controls (encryption, audit logging, access control, data minimization) and dedicated compliance-review agent specs. These are engineering checklists — not legal certifications.
- Services handling sensitive data must document data classification in `templates/docs/data-classification-template.md` and satisfy `standards/compliance-engineering.md` and `standards/hipaa-controls.md` where applicable.

Onboarding / how to use in a new repo
1. Read `templates/docs/repo-instructions-template.md` and `standards/engineering-principles.md`.
2. Run the scaffolder agent or generator: `python tooling/scripts/generate-template.py --stack <java|python> --name <SERVICE>` (or use `agents/backend-service-builder`).
3. Implement or review `ConfigProvider` wiring, provide cloud adapters and explicit local fallbacks, and add tests.
4. Run validators: `tooling/scripts/validate-repo-structure.ps1` and CI checks in `.github/workflows/`.
5. Use `agents/code-reviewer` and `agents/compliance-reviewer` to validate before production rollout.

See `docs/overview.md` and `standards/` for full rules and checklists.

---

Using in other projects with VS Code Copilot
---------------------------------------------

Every project that should follow these standards can wire them into VS Code Copilot in three steps, with no duplication of content.

### How it works

VS Code Copilot auto-loads `.github/copilot-instructions.md` from the workspace root on every chat. By placing a lightweight bootstrap file in each project's `.github/` folder that references this standards repo, Copilot will enforce all org rules, layer constraints, naming standards, fallback requirements, and compliance checklists automatically — without copying any content.

### Step 1 — Copy the bootstrap template

```
cp enterprise-ai-engineering/templates/docs/project-copilot-instructions-bootstrap.md \
   <your-project>/.github/copilot-instructions.md
```

Or manually copy `templates/docs/project-copilot-instructions-bootstrap.md` and place it at `.github/copilot-instructions.md` in the target project.

### Step 2 — Update the standards repo path

Open the file and replace `{STANDARDS_REPO}` with the relative or absolute path to your local clone of this repo. Example:

```markdown
> **Standards repo path:** `../../shared/enterprise-ai-engineering`
```

The path only needs to be readable on the developer's local machine — Copilot follows the markdown link references when responding in that workspace.

### Step 3 — Optionally install slash commands

Copy the prompt files to get `/scaffold-service` and `/compliance-review` slash commands in the target project:

```
cp enterprise-ai-engineering/.github/prompts/*.prompt.md \
   <your-project>/.github/prompts/
```

### What Copilot will do automatically once wired

| Trigger | Copilot behavior |
|---------|-----------------|
| Any chat in the project | Enforces 5-layer architecture, capability interfaces, fallback toggles |
| Editing a `.java` file | Applies Java naming, constructor injection, 30-line method, Testcontainers rules |
| Editing a `.py` file | Applies Python `Depends()` DI, Pydantic v2, async, structlog rules |
| `/scaffold-service` | Generates a complete new service with all standards baked in |
| `/compliance-review` | Audits the current service against HIPAA and security checklists |

### What you do NOT need to do

- Do not copy `core/`, `standards/`, or `stacks/` into the target project.
- Do not maintain duplicate standards — all updates happen in this repo and take effect in every wired project immediately.
- Do not add language-specific `.instructions.md` files manually — copy them from `.github/instructions/` if you want per-file-type auto-attachment.

---

VS Code agent files reference
------------------------------

| File | Location in this repo | Purpose |
|------|----------------------|---------|
| Master instructions | `.github/copilot-instructions.md` | Auto-loaded in every chat in this workspace |
| Java rules | `.github/instructions/java-standards.instructions.md` | Auto-attached to any `.java` file |
| Python rules | `.github/instructions/python-standards.instructions.md` | Auto-attached to any `.py` file |
| New service checklist | `.github/instructions/new-service.instructions.md` | On-demand when creating services |
| Scaffold prompt | `.github/prompts/scaffold-service.prompt.md` | `/scaffold-service` slash command |
| Compliance prompt | `.github/prompts/compliance-review.prompt.md` | `/compliance-review` slash command |

