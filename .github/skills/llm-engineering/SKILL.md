---
name: llm-engineering
description: Use when work involves LLM/model-backed behavior, RAG, agents or tool calling, an AI/model gateway, LLM evaluation, or AI-specific tracing and observability. Covers only AI-specific concerns; compose with the general skills listed inside.
---

# LLM Engineering

Apply only the sections the approved requirements call for. Everything here is a consideration for planning and review, not a requirement: a threshold, metric, fallback, or control enters scope only when the requirements state it. When a material AI behavior is unspecified (for example an evaluation threshold or what happens with insufficient context), ask; do not choose.

## Composes With

Use the general skill for the general concern; this skill adds only the AI-specific part.

| Work | Compose with |
| --- | --- |
| AI gateway | `api-design`, `architecture-design`, `resilience-and-degradation`, `security`, `observability` |
| LLM evaluation | `testing` |
| AI tracing / evaluation platform | `observability` |
| RAG | `testing`, plus `architecture-design` or data skills where retrieval storage changes |
| Agentic workflow | `security`, `resilience-and-degradation`, `distributed-systems` — only where those concerns apply |

## Model and Prompt Behavior

- Model, provider, version, and parameters (for example temperature or output limits) can change behavior. Where they are part of an implementation decision, they are recorded and traceable, as are the prompts and system instructions.
- A different model or provider is not behaviorally equivalent. A substitution is a behavior change: it needs requirement approval and evaluation evidence.

## Evaluation

- Name what is evaluated: correctness, faithfulness/grounding, retrieval quality, tool selection, hallucination, safety, latency, or cost.
- Version the evaluation dataset or representative cases with the code.
- Keep deterministic assertions separate from model- or judge-based evaluation; record the judge's model and prompt.
- Acceptance thresholds come from the requirements. Where outputs are nondeterministic, state how many runs and what pass rate count as passing.
- Record model, prompt, parameters, dataset version, and results so later runs can be compared. Any framework may be used; none is required.

## RAG and Grounding

- Retrieval quality and answer quality are separate concerns, evaluated separately.
- When grounding is required, test that answers cite or stay within retrieved sources.
- Behavior with no or insufficient context (refuse, ask, or answer with a caveat) is stated in the requirements, never assumed.

## Agents and Tools

- Each tool has an explicit contract and authorization boundary; the model never gains authority the caller lacks.
- Side-effecting tool calls need idempotency or duplicate protection under retries, and human approval where the requirements require it.
- Loops have an explicit termination bound (steps, time, or cost).
- Define the outcome of tool or model failure mid-run, including partial completion.

## AI Gateway

Applies only when the requirements call for central model routing, cost tracking, or fallback; do not propose a gateway otherwise.

- Routing: how a request selects model and provider. Fallback to a different model is a behavior change (Model and Prompt Behavior), not only a resilience setting.
- Token and cost attribution per request, and per tenant, user, or feature where required; budgets or quotas only when required.
- Provider rate limits, timeouts, and outages: the required behavior for each.
- Streaming: whether retry or fallback is possible after part of a response has been sent.
- Caching identical or similar requests can return stale answers or expose one caller's data to another; caching is opt-in per requirement.
- Provider credentials stay inside the gateway; callers never receive them.

## AI Operations

- Trace model calls, tool calls, and retrieval where operationally relevant, with latency and token/cost evidence where material.
- Prompts, responses, retrieved context, and tool outputs may contain sensitive data: redact or exclude them from logs and traces as the security requirements require.
