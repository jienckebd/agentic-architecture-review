# Knowledge, state, and tool boundaries

Use this reference when reviewing durable knowledge, protocol state, retrieval shared across runs or agents, tool catalogues, or a proposed knowledge graph.

## Contents

- Select the smallest useful knowledge architecture
- Decide whether a graph earns itself
- Design graph truth safely
- Make protocol state explicit
- Design tools for nondeterministic callers
- Required review output

## Select the smallest useful knowledge architecture

Keep these concerns separate:

- **Canonical records:** governed entities, calculations, ownership, and current product truth.
- **Evidence store:** source snapshots and provenance supporting material claims.
- **Retrieval index:** a derived access path optimized for recall and relevance, not authoritative truth.
- **Conversation context:** temporary information useful within the current interaction.
- **Workflow state:** durable checkpoints, approvals, retries, and completion evidence.
- **Relationship graph:** durable entities and typed edges queried across agents, workflows, or sessions.

Use records and ordinary joins when they answer the required queries well. A graph-shaped domain model does not require a graph database.

Review retrieval independently from generation: authorization before retrieval, source freshness and provenance, recall and precision by slice, reranking, context budgets, and behaviour when evidence is absent or conflicting.

## Decide whether a graph earns itself

A knowledge graph is a candidate when one or more measured constraints are binding:

- Several agents or workflows repeatedly query the same entities and relationships.
- Work spans sessions and transcript replay or summary handoff loses important state.
- Relationship traversal is central to the product outcome.
- Evaluators need claim-level grounding against durable, attributable relationships.
- Orchestrator context is saturated by summaries from workers.
- Historical contradictions and supersession must remain queryable.

Require representative queries and a comparison with relational records, typed edge tables, or retrieval. Reject a phantom graph that is written but rarely queried, duplicates a system of record, or has no measurable effect on quality, context use, or operability.

Count the complete burden: ingestion, entity resolution, ontology changes, authorization, migrations, query latency, operations, and error correction.

## Design graph truth safely

If a graph is selected:

- Use canonical identifiers before fuzzy entity matching.
- Define node and edge types, ownership, validation, and temporal meaning.
- Attach source provenance, extraction version, confidence, and observed time to material claims.
- Prefer additive or versioned claims with `supports`, `contradicts`, and `supersedes` semantics instead of silent overwrite.
- Represent conflicts and uncertainty rather than forcing one fact prematurely.
- Enforce source permissions during traversal and synthesis, not only during ingestion.
- Provide correction, deletion, retention, and schema-migration paths.
- Evaluate graph extraction, entity resolution, retrieval, grounding, and downstream outcomes separately.

A graph preserves errors as effectively as facts. Do not treat durability as correctness.

## Make protocol state explicit

An application can be stateful while its protocol remains stateless. Review hidden sessions against explicit, opaque state handles.

A handle should identify a resource, never grant access to it. Authenticate and authorize every use. Define tenant and record scope, expiry, revocation, concurrency behaviour, replay semantics, retention, and cleanup for orphaned resources. Do not hide critical state from the component responsible for planning or recovery.

Compare provider-managed and application-managed state on portability, observability, replay, deletion, residency, cost, and operational control. Avoid making an unstable provider representation the canonical domain record.

## Design tools for nondeterministic callers

Tool descriptions and schemas influence model behaviour and are part of the effective prompt. Review:

- Capability-oriented names and namespaces that make selection unambiguous.
- The smallest catalogue needed for the task; more tools can reduce reliability.
- Typed arguments with stable identifiers, explicit state handles, defaults, limits, and side-effect declarations.
- Decision-ready, token-efficient results rather than unfiltered API payloads.
- Structured errors that distinguish retryable, permanent, denied, stale, and invalid requests.
- Idempotency, read-after-write verification, and recovery semantics.
- Real-agent tool-use trials, including held-out, ambiguous, and adversarial cases.

## Required review output

State which store owns each kind of truth, how state is addressed, and why each tool or index exists. If recommending a graph, include the queries that earn it, the simpler alternative tested, its permission and provenance model, and the evidence that will justify continued operation.
