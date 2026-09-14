# Verification and evaluation

Use this reference to decide whether an agentic loop or added architecture has earned its autonomy and cost.

## Verification determines autonomy

Classify the strongest acceptance signal available to each loop:

1. **Formal verifier:** a proof, schema, invariant, compiler, or deterministic policy check.
2. **Execution feedback:** tests, read-after-write confirmation, environment state, or observed business outcome.
3. **Learned or human judge:** a calibrated model grader or domain expert applying a stable rubric.
4. **Intrinsic confidence:** self-critique, self-consistency, confidence, or agreement without external grounding.

Use the strongest available signal. Move a loop toward stronger verification before increasing autonomy. Intrinsic confidence can propose a revision but should not authorize consequential actions or persistent self-change.

For every evaluator or critic, record what it observes, what it cannot observe, its calibration evidence, and whether it shares a model, prompt, context, or systematic bias with the generator.

## Earn architectural complexity through error analysis

Before adding a planner, critic, specialist, graph, or delegation layer:

1. Establish the simplest credible baseline.
2. Run representative trials and inspect their traces and actual outcomes.
3. Open-code observed failures, then group and count recurring failure classes.
4. Locate each failure in the model, prompt, context, retrieval, tool contract, workflow, state, permission, or verification layer.
5. Add the smallest change that targets the demonstrated failure.
6. Re-run the same cases and meaningful slices against the baseline.

If individual steps are strong but the end-to-end result is weak, inspect workflow composition. If the same failure occurs inside one component, do not hide it behind another agent. Periodically test whether model or tool improvements allow obsolete scaffolding to be deleted.

## Evaluate stochastic systems

Keep these concepts distinct:

- **Task:** the stable problem specification.
- **Trial:** one stochastic attempt at the task.
- **Transcript:** the calls, decisions, messages, and tool activity during a trial.
- **Outcome:** the resulting environment or product state.
- **Grader:** the mechanism that scores a transcript, outcome, or both.
- **Harness:** the prompts, tools, runtime, policies, and scaffolding surrounding the model.

Run enough trials to expose meaningful variance for the decision at hand. A transcript claiming success is not evidence that the outcome occurred; verify consequential outcomes independently.

Compare candidates with inexpensive alternatives such as a direct structured call, retry, retrieval improvement, better tool contract, or escalation to a stronger model. Report quality, critical failures, latency, tokens, tool calls, and cost by case and slice. Prefer a Pareto-efficient design rather than optimizing quality without regard to operating cost.

## Required review output

For every material loop or architecture addition, name:

- The failure class it addresses.
- The acceptance signal and its verification level.
- The baseline and number of trials used for comparison.
- Transcript and outcome checks.
- Quality, latency, and cost trade-offs.
- The evidence required to retain, remove, or expand the pattern.
