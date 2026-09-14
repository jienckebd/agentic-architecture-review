---
name: agentic-architecture-review
description: "Reviews or redesigns agentic system architectures and implementation plans using current primary-source research. Use when deciding agent, sub-agent, workflow, model-call, tool, state, approval, tracing, golden-dataset, or evaluation boundaries. Do not use for ordinary code review or a narrow feature with no agentic architecture decision."
---

# Agentic architecture review

Produce an evidence-backed architecture that is no more agentic than the problem requires, then make sure the implementation plan can deliver it.

## Select the review mode

- **Architecture review:** assess a current or proposed system and recommend a target design.
- **Implementation-plan review:** test whether a plan completely and correctly implements an agreed architecture.
- **Combined review:** establish the target architecture, then edit or write the implementation plan to match it.

If the user asks to update a document, edit it. If the user asks only for feedback, do not change files.

The user's explicit instructions and architecture constraints take precedence over this skill's defaults. Review within those constraints and report material trade-offs. Do not silently replace a user-mandated topology with a preferred one.

## Establish the real system

Inspect the repository, current diagrams, runtime dependencies, data contracts, integrations, and deployment model. Treat diagrams and planning documents as claims to verify against code. Preserve product-specific requirements, existing authorization boundaries, and useful infrastructure unless the evidence supports replacing them.

Before evaluating topology, identify:

- The jobs the product must complete and who uses each outcome.
- Data sources, governed metrics, evidence, and source ownership.
- Read-only work, drafts, external writes, and irreversible actions.
- Latency, scale, privacy, permission, reliability, and cost constraints.
- Which outputs are deterministic and which require judgement.

## Research current practice

Agent runtimes and model capabilities change quickly. When the request concerns current or best architecture, browse current primary sources. Prefer official runtime and cloud architecture documentation, provider engineering guidance, standards, and research papers. Do not base the recommendation on consultancy summaries, listicles, or vendor comparison blogs.

Compare principles across sources rather than copying one provider's reference architecture. Record the review date and link claims to the source that supports them. Treat framework selection as a consequence of requirements, not the starting point.

## Classify before designing

Classify every proposed component as one of:

- Deterministic code or service.
- Structured model call.
- Code-defined workflow containing model calls.
- Tool exposed through a typed contract.
- Evaluator or critic node.
- Agent with a bounded model-directed tool loop.

An agent is justified when the path cannot be usefully specified in advance and the model must choose a changing sequence of tools to reach an outcome. Recommend a sub-agent when evaluation shows a meaningful quality gain or it creates a real isolation boundary such as identity, permissions, tools, context, model policy, or deployment. Do not default to agents for personas, pipeline stages, file formats, or deterministic routing.

Start with the least complex topology that can pass the evaluation set. Prefer sequential or parallel workflow control in code when the graph is known. Cap evaluator revision loops. Do not default to recursive delegation or unbounded planning. If the user's requirements genuinely need recursive delegation, define and test strict limits for depth, breadth, permissions, time, tokens, and spend.

Read [references/topology-decision.md](references/topology-decision.md) whenever the review must choose among a workflow, single agent, multi-agent system, handoff, or orchestrator with delegated workers. Apply the decision tests and state the trade-off or evidence behind patterns that were not selected.

Read [references/verification-and-evaluation.md](references/verification-and-evaluation.md) when deciding whether autonomy or architectural complexity is justified. Require trace-led error analysis, repeated trials for stochastic behaviour, independent outcome checks, and comparison with simple cost-controlled baselines. The strength of the verifier limits the safe autonomy of the loop.

Read [references/knowledge-state-and-tools.md](references/knowledge-state-and-tools.md) when the design includes durable knowledge, protocol or tool state, retrieval shared across agents, or a proposed knowledge graph. Treat graph storage as an earned response to repeated relationship queries or a measured coordination bottleneck, not as the default memory layer.

Read [references/adaptive-recovery.md](references/adaptive-recovery.md) when a proposal uses “self-healing,” reflection, automatic repair, cross-run learning, or modification of memory, prompts, tools, workflows, code, evaluators, or policy. Separate deterministic recovery, bounded output repair, and persistent system improvement; apply controls proportional to what the loop can change.

## Review the whole operating system

Read [references/review-rubric.md](references/review-rubric.md) and assess every applicable section. The review is incomplete if it covers topology but omits data truth, durable state, permissions, live tracing, the golden dataset, evaluations, or production operations.

For implementation plans, confirm that architectural promises appear as owned build work with dependencies, deliverables, release gates, and observable exit criteria. “Add evals later” and “monitor in production” are not implementation steps.

## Produce a decision, not a catalogue

Lead with the recommended architecture and whether the current approach should be retained, revised, or replaced. Include:

1. Product and constraint summary.
2. Current-state findings supported by repository evidence.
3. Component classification and topology decision.
4. Target architecture and state boundaries.
5. Safety, approval, tracing, golden-data, and evaluation design.
6. Implementation-plan gaps and ordered changes.
7. Decisions that require a named business or technical owner.
8. Dated primary sources.

Use **satisfied**, **partial**, **missing**, or **not applicable** for checklist findings. Do not hide false precision behind a single architecture score.

When editing an implementation plan:

- Preserve verified business requirements and replace contradicted architectural language.
- Make phases vertical and testable where practical.
- Put schemas, evaluation fixtures, permission policy, and runtime recovery work before broad UI construction.
- Give each phase an exit criterion that can fail.
- Add unresolved policy decisions without treating them as technical blockers when work can safely continue.
- Run the repository's relevant document checks before handoff.

## Keep the recommendation honest

Separate sourced facts, repository observations, recommendations, assumptions, and unresolved decisions. Name trade-offs in latency, cost, reliability, operational load, and permissions. Do not claim one framework is universally best. If evidence cannot distinguish two runtime options, define a bounded technical spike with pass and fail criteria.

## Validate changes to this skill

Use [evals/cases.json](evals/cases.json) for behavioural forward tests with and without the skill on each intended model and surface. Do not claim behavioural validation unless those cases have actually been run. After editing either project copy, run `python scripts/validate_skill.py` from that skill directory to check the evaluation fixtures, reference navigation, and Codex-Claude parity.
