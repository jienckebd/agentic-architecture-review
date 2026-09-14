# Topology decision guide

Choose topology per outcome or workflow stage. A production system can combine deterministic workflows, model calls, and one or more agents without labelling the whole graph as one pattern.

## Contents

- Start with five questions
- Decision matrix
- Deterministic workflow
- Single agent
- Multi-agent system
- Orchestrator with delegated workers
- Router, handoff, and worker are different
- Required review output

## Start with six questions

1. Can code define the useful steps, branches, and stopping condition before the run starts?
2. Must a model choose a changing sequence of tools based on intermediate results?
3. Can one identity, permission set, context boundary, and tool set complete the work well?
4. Are specialist boundaries known before the run, or must they be discovered from the task?
5. Does evaluation show that extra coordination improves quality enough to justify its latency, cost, security, and reliability burden?
6. What independently verifies success, and is that signal strong enough for the proposed autonomy?

Use the answers to select the least complex pattern below.

## Decision matrix

| Pattern | Use when | Do not use when | Control owner |
|---|---|---|---|
| Deterministic workflow | Steps, branches, parallelism, and stopping rules are known | A model must discover the path while working | Application code |
| Single agent | The path varies and one bounded agent can choose tools within one coherent authority and context | A structured model call or known workflow can finish the job | One model-directed loop |
| Multi-agent system | Separate specialists need materially different tools, identity, permissions, context, model policy, or deployment, and evaluation proves the split | The proposed agents differ only by persona, pipeline stage, or output format | Explicit coordination contract |
| Orchestrator with delegated workers | The orchestrator must discover and decompose an unknown set of independent subtasks, delegate them, then synthesize their results | The subtasks are a known list or fixed fan-out such as one assessment per deal | Orchestrator agent, within hard delegation limits |
| Handoff | A specialist should become the active owner of the conversation or case | A central agent merely needs a specialist result and should retain responsibility | Receiving specialist |

## Deterministic workflow

Use a workflow when the graph is known even if some nodes use models. Common forms are:

- Sequential stages with typed inputs and outputs.
- Conditional routing from rules or a bounded classifier.
- Parallel fan-out and deterministic join.
- A capped generator and evaluator revision loop.
- Human approval as a persisted workflow pause.

A model call inside a workflow does not make the node an agent. A workflow is usually the right choice for extraction pipelines, per-record assessment, governed calculations, document rendering, validation, approval, and external-system verification.

Prefer a workflow when reproducibility, predictable cost, low latency, auditability, or exact recovery matters. Do not add an LLM supervisor to choose a sequence that the application already knows.

## Single agent

Use one agent when intermediate evidence changes which tool should run next and enumerating every valid path would make the workflow brittle. Keep the agent bounded by:

- One explicit outcome and stopping condition.
- A capability-scoped tool set rather than the full company catalogue.
- Server-enforced identity, record scope, and side-effect policy.
- Typed tool contracts and durable tool results.
- Turn, time, token, retry, and cost budgets.
- A persisted approval point immediately before external side effects.

Try this topology before a multi-agent split. If one agent fails, use traces and component evaluations to establish whether the cause is context overload, conflicting instructions, tool ambiguity, model capability, or a genuine security boundary.

## Multi-agent system

Multi-agent is an umbrella term, not a reason to create a team of personas. Use it only when at least one of these boundaries is real:

- Different service identities or authorization scopes.
- Mutually exclusive tools or data access.
- Contexts that should not be shared for privacy, safety, or performance.
- Different models or policies with measured task-specific advantages.
- Independent deployment, ownership, scaling, or failure isolation.
- Specialist quality that is measurably better than a single-agent baseline.
- A specialist catches a distinct recurring error class that the shared agent does not.

Agents communicate through typed tasks and bounded result artifacts, stable record IDs, and explicit evidence references. Do not pass full transcripts by default, rely on shared hidden conversation state, or let several agents mutate the same record without concurrency control. Count total context and tokens rather than agent count alone.

Evaluate the multi-agent candidate against the single-agent or workflow baseline on correctness, critical failures, latency, cost, tool calls, and recovery. Reject the split if it merely moves prompt complexity into coordination.

## Orchestrator with delegated workers

Use an agentic orchestrator only when the number or shape of subtasks cannot be known until the request is interpreted or intermediate results arrive. The orchestrator retains the objective, creates bounded task contracts, selects workers, collects results, resolves gaps, and produces the final synthesis.

Delegated workers should:

- Receive a narrow task, evidence scope, permitted tools, output schema, and budget.
- Return a bounded, decision-ready, evidence-backed artifact or a clear failure without changing the parent objective.
- Avoid delegating again unless a reviewed design explicitly permits one bounded level.
- Have side effects disabled by default; centralize approval and execution policy.

Set limits for worker count, delegation depth, parallelism, repeated tasks, time, tokens, and spend. Persist the task graph and parent-child traces. The orchestrator must be able to finish with partial worker failure and must not repeatedly create workers to repair the same unresolved gap.

Do not use agentic orchestration for a known fan-out. Assessing every deal, processing every document, or calling three known specialists is application-controlled parallel workflow work.

## Router, handoff, and worker are different

- A **router** selects among known paths. Use deterministic rules first and a structured classifier when intent genuinely requires judgement.
- A **delegated worker** completes a bounded task and returns its result to the orchestrator, which remains responsible for the outcome.
- A **handoff** transfers active ownership to another agent because that specialist should control subsequent conversation and tools.
- A **tool** performs a capability under the caller's control. A PDF builder, email drafter, database query, or CRM change-set generator is usually a tool or workflow, not a worker agent.

Use handoffs sparingly in business applications because ownership, permissions, trace continuity, and user expectations become harder to reason about after control changes.

## Required review output

For every important component, report:

| Component | Selected pattern | Why it needs that pattern | Simpler pattern considered | Evidence or evaluation required |
|---|---|---|---|---|

If multi-agent or orchestrator-workers is selected, also document:

- Worker boundaries and permitted tools.
- Task and result schemas.
- Parent and child state ownership.
- Coordination, retry, partial-failure, and cancellation behaviour.
- Delegation limits and stopping conditions.
- Approval ownership and side-effect policy.
- The baseline and evaluation threshold that justify the added topology.
