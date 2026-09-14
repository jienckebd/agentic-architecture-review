# Recovery and adaptive loops

Use this reference when a proposal describes self-healing, reflection, automatic repair, cross-run learning, or a system that can modify its own operating components.

## Classify the loop before reviewing it

“Self-healing” can mean three different systems:

1. **Runtime recovery:** deterministic retry, checkpoint resume, fallback, reconciliation, duplicate-write prevention, or dead-letter handling.
2. **Output repair:** generate, verify, revise, and stop within one task.
3. **Persistent system improvement:** production evidence changes memory, prompts, skills, tools, workflows, code, evaluators, or policy across future runs.

Use ordinary workflow recovery for the first category. Use a bounded evaluator-optimizer for the second. Treat the third as a governed change-management system, not as a larger retry loop.

## Controls for every repair loop

Define:

- The immutable task, policy, and acceptance criteria.
- What failure signal starts the loop and its verification strength.
- What the loop may inspect and change.
- The state and completed work preserved across attempts.
- Maximum revisions, retries, time, tokens, and spend.
- Escalation and safe terminal states when repair fails.
- Trace links between the original failure, each attempted repair, and the verified outcome.

Run deterministic checks before subjective graders. Preserve successful work across replans. A model's claim that it repaired something is not outcome verification.

## Persistent improvement requires a stronger boundary

Classify both the modifiable surface and degree of loop closure:

- **Surface:** output, memory, harness, model, evaluator, or policy.
- **Closure:** human-in-the-loop, human-on-the-loop, or closed loop.

As the surface expands or human review recedes, require stronger external verification. Keep the objective, authorization policy, deployment gate, and safety controls outside the component that can modify itself.

Persistent proposals should be versioned and evaluated against development and private holdout cases. Use independent outcome checks, human or policy approval proportional to risk, canary release, monitoring, and automatic or operator rollback. Record who accepted the change and why.

## Prevent self-confirming loops

Generator and evaluator biases may correlate, especially when they share a model, prompt, context, or training lineage. Role labels alone do not create independence.

Mitigate this by:

- Grounding acceptance in formal checks, execution results, business outcomes, or expert labels.
- Separating generator and evaluator context where useful.
- Calibrating learned judges and tracking false passes.
- Scoring environmental outcomes rather than transcript claims.
- Using a visible development score and a protected acceptance score when the system can optimize against the rubric.
- Sampling traces for human error analysis and promoting verified failures into the golden dataset.

Do not permit a system to rewrite its own definition of success, approval policy, or release gate and then approve that change with the same loop.

## Required review output

Report the loop category, modifiable surface, closure level, grounding signal, budgets, escalation path, persistence, release mechanism, and rollback. If the proposal uses “self-healing” without specifying these properties, mark it missing rather than treating the label as an architecture.
