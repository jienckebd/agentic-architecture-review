# Review rubric

Use the applicable sections for architecture reviews and implementation-plan reviews. A plan passes only when important architectural requirements have concrete implementation work and exit criteria.

## Contents

- Product contract
- Component boundaries
- Data, evidence, and memory
- Runtime and recovery
- Runtime primitive ledger
- Code shape
- Permissions and side effects
- Live tracing and operations
- Golden dataset
- Evaluations
- Implementation plan
- Common failure patterns

## Product contract

- Users, jobs, decisions, and actions are explicit.
- Role-specific views use the same underlying truth where appropriate.
- Inputs, outputs, evidence requirements, uncertainty, and failure behaviour are defined.
- Success measures cover usefulness and correctness, not feature delivery alone.
- Out-of-scope work and policy decisions are visible.

## Component boundaries

- Deterministic calculations remain deterministic.
- Structured judgement uses validated model outputs.
- Known sequences and routing use code-defined workflows.
- Independent work can fan out and join without model coordination.
- An agent owns only work that needs dynamic planning or tool choice.
- Tools have narrow descriptions, typed inputs, typed outputs, side-effect declarations, and retry semantics.
- Tool names, namespaces, descriptions, and result shapes are tested with real agent callers; the catalogue is no larger than the task requires.
- Tool results are decision-ready and token-efficient rather than unrestricted API payloads.
- Critics have explicit criteria and a capped number of revisions.
- Every agent or proposed sub-agent has a measurable or security-based reason to exist.
- Every specialist addresses a distinct observed failure class or enforceable isolation boundary.
- Agent, turn, time, token, retry, and cost limits are defined.

## Data, evidence, and memory

- A canonical domain record exists for shared product truth.
- Governed calculations name their source of truth.
- Entity resolution uses stable identifiers before fuzzy matching.
- Uncertain matches remain uncertain and can be corrected.
- Material claims link to evidence and an evidence-snapshot version.
- Missing, unavailable, denied, stale, and empty data remain distinct states.
- Domain state, durable workflow checkpoints, and conversation state are separate.
- Protocol state is explicit and addressable; handles identify resources without granting access and have scope, authorization, expiry, revocation, and cleanup rules.
- Context packets contain the minimum relevant evidence and policy rather than unrestricted histories.
- Retrieval authorization, provenance, freshness, recall, precision, reranking, and context budgets are evaluated separately from generation.
- A knowledge graph is used only when representative relationship queries, cross-session persistence, or shared-agent state outperform simpler records or typed edges.
- Graph claims retain provenance, time, confidence, contradictions, and supersession; graph traversal enforces source permissions.
- Retention, redaction, deletion, and access rules follow source-specific requirements.

## Runtime and recovery

- Long-running work is checkpointed outside the process.
- The same workflow supports scheduled and on-demand runs.
- Activities are idempotent and external writes have stable idempotency keys.
- Approval waits survive restarts and deployments.
- Retries distinguish transient, permanent, policy, and data-quality failures.
- Partial failure does not discard unrelated completed work.
- Plans validate dependencies against available tools, preserve completed steps across replanning, and escalate after bounded repeated failure.
- Previous good results remain available when refresh fails and are marked stale.
- Concurrency, source rate limits, dead letters, cancellation, and backpressure are covered.
- A runtime choice is proven with pause, restart, replay, and duplicate-write tests.
- Hand-written checkpointing, replay, interrupt, retry, concurrency, or tracing code is **partial** until the primitive ledger names the maintained primitive considered and the measured reason it was rejected.
- Features the maintained primitive provided and the hand-rolled path dropped are listed and either rebuilt or accepted by name.
- A decision record that names a runtime matches the code that runs; a contradiction is reported before either is rewritten.
- Prompts, tool schemas, policies, and model snapshots are versioned; the version is part of every replay key and span, so a mid-run change cannot replay stale output unnoticed.

## Runtime primitive ledger

Fill one row per runtime capability the system needs. Check the repository's existing dependencies before treating a primitive as new.

| Capability | Maintained primitive (in repo already?) | Adoption cost | Hand-rolled cost | Features dropped by hand-rolling | Decision and observable reversal trigger |
|---|---|---|---|---|---|

Capabilities to consider: durable checkpoint and resume, replay of completed steps, human-in-the-loop interrupt, retry policy, timeout and concurrency budget, trace and span propagation, structured-output validation, tool protocol.

Skip a capability when the ledger shows no requirement for it: no resume, interrupt, or branching need, or rerun-from-scratch cost below the primitive's operating cost. Say so in the decision column.

## Code shape

- One persistence path per concern; wrappers or stores duplicated per stage are counted and consolidated.
- Infrastructure copied between services is named as a shared dependency or deleted.
- Each direct dependency has a stated reason; two drivers or two state stores for one concern are a finding.
- Idempotency is enforced by a constraint or upsert, not by select-then-insert.
- Serialization for cache or step keys is canonical and shared, not re-implemented per call site.

## Permissions and side effects

- The signed-in user's scope is enforced by the server, not the prompt.
- Managers and delegates have an explicit, verified authority model.
- Source content is treated as untrusted data, never as agent instruction.
- Each tool invocation receives the minimum record scope and capability set.
- Read, draft, external-write, destructive, and scope-expanding actions have separate policies.
- Blocking checks run before side effects and validate arguments, authorization, scope, approval, and idempotency.
- Approval shows the exact recipient, record, content or diff, evidence, and expected effect.
- Execution is verified by reading back the external result and recording completion evidence.
- Secrets and restricted evidence are absent from exported telemetry and model context unless required.

## Live tracing and operations

- A trace ID follows the API request, workflow, source calls, model calls, tools, policies, approvals, retries, and completion checks.
- Trace context survives async boundaries, checkpoints, and approval waits.
- Product progress comes from persisted workflow events rather than log scraping.
- Parent and child spans record configuration versions, duration, tokens, cost, status, retries, and stopping reason.
- Tool calls, model decisions, state transitions, handoffs, memory operations, and context compaction are observable as typed spans or events.
- Evidence identifiers or hashes provide provenance without copying unrestricted content into telemetry.
- Trace access follows product permissions and redaction policy.
- Trace content passes through one field-level, default-deny redaction boundary with per-field retention rules.
- Head or tail sampling preserves errors, slow runs, critical workflows, and required regulated records according to explicit policy.
- Dashboards cover completion, latency, failures, critic rejection, cost, approval waits, stale results, and duplicate-write prevention.
- Alerts link directly to a run and trace.

## Golden dataset

- Scenario names expand into multiple replayable cases rather than single prompts.
- Each case freezes the user request, role, scope, policy version, source availability, evidence snapshot, and governed facts.
- Expected fields, acceptable alternatives, required citations, forbidden claims, allowed tools, approvals, and terminal state are labelled.
- Cases cover ordinary, sparse, conflicting, stale, unavailable, adversarial, rejected-approval, retry, and partial-failure conditions.
- Dataset slices expose differences by user role, workflow, data coverage, outcome class, lifecycle state, or another meaningful domain cohort.
- Development and holdout sets are separate.
- Label agreement is measured against the rubric before scaling labels or calibrating judges.
- Contamination, holdout leakage, and near-duplicate cases are detected rather than silently reweighting results.
- Domain experts own domain labels; engineering owns fixture integrity; the evaluation owner maintains rubrics and judge calibration.
- Production failures enter the set only after permission-safe capture, de-identification, labelling, review, and versioning.
- Cases have owners, provenance, change history, and disputed-label handling.
- Coverage, production drift, stale labels, duplicates, and obsolete cases are audited on a defined refresh and retirement cadence.

## Evaluations

- Deterministic assertions cover schemas, calculations, permissions, contracts, state transitions, and idempotency.
- Component evaluations isolate retrieval, extraction, assessment, critique, planning, and artifact generation.
- Workflow evaluations inspect tool selection, arguments, unnecessary calls, approvals, stopping behaviour, and recovery.
- Architecture changes begin with trace-led error analysis that names and counts the recurring failure class each added stage is intended to fix.
- Product evaluations ask domain experts whether results are correct, useful, appropriately uncertain, and actionable.
- Groundedness and citation validity are evaluated for material claims.
- Domain scores, probabilities, classifications, and confidence are evaluated separately and calibrated against observed outcomes when available.
- Model judges are calibrated against expert labels, with disagreement and false-pass rates tracked.
- Candidate runs compare with the current production baseline by case and slice, including latency and cost.
- Stochastic candidates run enough repeated trials to expose relevant variance; transcripts and external outcomes are evaluated independently.
- Agentic candidates are compared with direct structured calls, retries, retrieval or tool improvements, and model escalation on a quality-cost-latency Pareto basis.
- Security evaluations include prompt injection in evidence, tool-argument tampering, scope expansion, approval bypass, and restricted-data leakage.
- Changes support shadow evaluation, canary release, rollback, and continuous sampling after launch.
- Adaptive loops classify what can change and their human-in, human-on, or closed-loop governance; persistent changes have an immutable objective and external acceptance gate.
- Critical invariants can block a release even when the aggregate score improves.

## Implementation plan

- The plan has a clear target architecture and component classification.
- Product schemas and source ownership precede dependent workflows.
- A versioned golden dataset and evaluation harness begin before prompt optimization.
- Live tracing is implemented with the first vertical slice.
- Permissions and approval policy are built before any external write is enabled.
- Runtime selection has requirements and a recovery spike rather than a framework preference alone.
- Each phase delivers an end-to-end capability where practical.
- Each phase names dependencies, deliverables, responsible owner or owner type, and a falsifiable exit criterion.
- Release gates include quality, security, reliability, latency, cost, and recovery.
- Migration, rollback, deletion of replaced paths, and operational ownership are covered.
- The plan includes evidence-based removal of scaffolding that no longer beats the simpler baseline.
- Unresolved business policy is named without hiding it in technical tasks.

## Common failure patterns

- A supervisor delegates fixed steps to several agents.
- Agents exist only to provide different personas or output formats.
- A whole portfolio is placed into one prompt and assessed in one response.
- Model-generated totals replace governed calculations.
- Conversation history is treated as durable domain truth.
- Tool permission is described in the prompt but not enforced by the server.
- A post-hoc guardrail is expected to stop a side effect that has already started.
- Tracing means logs without run correlation, source versions, or approval events.
- A golden dataset is a list of questions with no frozen evidence or labels.
- Evaluation relies only on an uncalibrated model judge or one aggregate score.
- The generator's confidence or a same-model critic is treated as independent proof of success.
- “Self-healing” conflates retry, output repair, and persistent system modification without separate controls.
- A knowledge graph is proposed without representative cross-agent or cross-session queries that earn its cost.
- The plan builds broad UI surfaces before proving one complete evidence-to-action path.
- Multi-agent topology is selected before a single-agent or deterministic baseline exists.
- A bespoke checkpoint table and replay wrapper sit beside a runtime checkpointer the repository already depends on.
- Several copies of one wrapper differ only by stage label.
- "No new frameworks" is treated as a requirement when the framework is already a dependency.
- A workflow runtime is added to a job that reruns from scratch cheaply and has no pause or branching.
