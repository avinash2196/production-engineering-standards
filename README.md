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
- `playbooks/` — step-by-step developer and operational workflows (create service, add endpoint, prepare for production).
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
- Fallbacks are explicit, toggled by environment variables (e.g., `FALLBACK_KAFKA=db`, `FALLBACK_CACHE=jsonfile`).
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

---

Slash Commands (type `/` in GitHub Copilot Chat)
-------------------------------------------------

All 15 slash commands live in `.github/prompts/`. Copy that folder into any project to activate them there.
Every command runs in **agent mode** — it reads standards files automatically and produces structured output.

### Getting started

```
/scaffold-service
```
The recommended first command for any new project. It asks 10 questions in a single message, then builds a full execution plan before writing a single file.

---

### Service creation

| Command | What it asks | What it produces |
|---------|-------------|-----------------|
| `/scaffold-service` | Service name, runtime (local Docker vs GCP Cloud Run), stack (Java/Python), messaging (Kafka vs Pub/Sub), cache (Redis vs Memorystore), storage (S3 vs GCS), secrets (Vault vs Secret Manager), database, API style, data classification | Numbered plan → creates every source file, test, Dockerfile, CI workflow, `.env.local`, and docs one by one with a live checklist |
| `/generate-adr` | Decision topic, context, options considered, chosen option | Structured ADR saved to `docs/decisions/ADR-NNN-<title>.md` using the org template |
| `/create-doc` | Doc type, audience, scope, existing inputs to reference, related docs to cross-link | New `.md` doc using the correct template from `templates/docs/` |

### Code quality

| Command | What it asks | What it produces |
|---------|-------------|-----------------|
| `/review-code` | Paste code or files, stack (java/python), compliance tier (standard/hipaa) | Line-level findings with severity (CRITICAL/HIGH/MEDIUM/LOW), standard violated, and fix |
| `/refactor-code` | Paste code to refactor, stack, refactoring goal | Refactored code with layering fixed, capability interfaces introduced, fallbacks wired |
| `/review-api-design` | Paste OpenAPI YAML/JSON, optionally previous version to diff | Naming, versioning, error format, HTTP verb findings + breaking-change diff |
| `/generate-tests` | Paste source file(s), stack, test type (unit/integration/contract/all) | Full test file(s) using mocks or Testcontainers, following org testing standards |
| `/generate-load-tests` | Service name, key endpoints + payloads, target RPS or concurrency, SLO targets | k6 or Gatling scripts establishing performance baselines |

### Architecture & systems

| Command | What it asks | What it produces |
|---------|-------------|-----------------|
| `/review-architecture` | Service name or paste architecture doc/ADR/source files | Findings on layer boundaries, abstraction usage, API design, dependency direction |
| `/review-distributed-systems` | Service name or paste source + dependencies | Idempotency, retry/timeout, failure modes, consistency model, async/sync boundary findings |
| `/analyse-codebase` | Repository path or paste key files, stack, analysis scope (full/architecture/security/observability) | Prioritised remediation report across architecture, fallbacks, observability, security, and test quality |
| `/maintenance-check` | Repository path or paste dependency manifest (`pom.xml` / `pyproject.toml`), stack | Outdated/vulnerable deps, observability gaps, deprecated APIs, standards drift, licence compliance |

### Compliance & security

| Command | What it asks | What it produces |
|---------|-------------|-----------------|
| `/compliance-review` | Service name, data categories (PHI/PII/internal/public), design doc or config files | Structured findings report with severity ratings and remediation steps against org compliance checklist |
| `/review-hipaa` | Service name, what PHI it handles, paste config or source files | HIPAA control audit: access control, audit logging, encryption, data minimisation, breach detection |
| `/review-production-readiness` | Service name or paste source + config files, target environment | Production readiness checklist: observability, resilience, config hygiene, deployment artifacts, health endpoints, test coverage |

---

### Example workflow for a new service

```
1. /scaffold-service
   → answers 10 questions
   → agent prints plan (24 files)
   → you confirm
   → agent creates files one by one with live checklist

2. /review-code
   → paste the generated service class
   → agent confirms standards compliance

3. /compliance-review
   → if handling PHI/PII — validates HIPAA controls

4. /review-production-readiness
   → before merging to main — final gate check
```

---

### Using slash commands in another project

1. Copy `.github/prompts/*.prompt.md` into your project's `.github/prompts/` folder.
2. Copy `.github/copilot-instructions.md` into your project's `.github/` folder and update the `{STANDARDS_REPO}` path to point to this repo.
3. Type `/` in Copilot Chat — all 15 commands appear immediately.

No duplication of `core/` or `standards/` is needed — commands reference this repo via relative links.

