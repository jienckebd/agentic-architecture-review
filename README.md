# Agentic architecture review

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill that reviews or redesigns agentic system architectures and implementation plans.

Its bias: **be no more agentic than the problem requires.** Most proposals that arrive labelled "multi-agent" are a fixed pipeline with personas attached. This skill makes you prove otherwise before it agrees, and it checks the parts of an agentic system that architecture documents usually skip: durable state, permissions, tracing, the golden dataset, and evaluations.

## What it actually does

Every proposed component gets classified as one of six things:

- Deterministic code or service
- Structured model call
- Code-defined workflow containing model calls
- Tool exposed through a typed contract
- Evaluator or critic node
- Agent with a bounded model-directed tool loop

An agent is only justified when the path cannot be usefully specified in advance and the model must choose a changing sequence of tools to reach an outcome. A sub-agent is only justified by a measured quality gain or a real isolation boundary (identity, permissions, tools, context, model policy, deployment). Personas, pipeline stages, file formats, and deterministic routing do not qualify.

Two principles do most of the work:

- **Verification strength caps autonomy.** A loop checked by a compiler or a read-after-write confirmation can be given more rope than one checked by the model's own confidence. Self-critique can propose a revision; it should not authorize a consequential action.
- **Complexity is earned through error analysis.** Establish a baseline, run trials, read the traces, group the actual failure classes, then add the smallest change targeting a demonstrated failure. Not a planner because planners sound thorough.

It also periodically asks the unpopular question: has a model or tool improvement made some of this scaffolding deletable?

The same rule runs the other way for infrastructure. Before it accepts hand-written checkpointing, replay, interrupts, retries, or tracing, it asks for a **runtime primitive ledger**: the maintained primitive that already does the job (checking the lockfile first, since a runtime already in the repo is not a "new framework"), what adopting it costs, what hand-rolling costs, and which features the hand-rolled version quietly dropped. Hand-rolling is allowed when the ledger shows it, for example when nothing needs to resume or a second database driver would be the price. Three copies of one wrapper differing by a stage label is a code-shape finding, not a runtime.

## Three modes

| Mode | Use for |
|---|---|
| Architecture review | Assess a current or proposed system, recommend a target design |
| Implementation-plan review | Test whether a plan actually delivers an agreed architecture |
| Combined review | Establish the target architecture, then edit the plan to match |

If you ask only for feedback, it does not touch your files.

Your explicit constraints win. If your regulator requires separate service identities for retrieval and writes, it reviews within that and reports the trade-off rather than quietly swapping in a topology it likes better.

## Install

```bash
git clone https://github.com/allierays/agentic-architecture-review.git \
  ~/.claude/skills/agentic-architecture-review
```

Project-scoped instead of personal:

```bash
git clone https://github.com/allierays/agentic-architecture-review.git \
  .claude/skills/agentic-architecture-review
```

The directory name has to stay `agentic-architecture-review` so it matches the `name:` in the frontmatter, which is why this repo is named the way it is. A bare `git clone` inside a `skills/` directory gets it right.

Verify it loaded with `/skills` in Claude Code.

## Use

Claude invokes it on its own when a request involves an agentic architecture decision. Or ask directly:

```
Review the architecture in docs/agent-design.md
Should this be one agent or three?
Does our implementation plan actually deliver the architecture we agreed?
Research current best practice for agent topology and update our plan
```

It will browse primary sources (official runtime and cloud architecture docs, provider engineering guidance, standards, papers) when the question is about current practice, and it dates what it cites. It deliberately ignores consultancy summaries and vendor comparison posts. Tell it not to browse and it will work from the repository alone.

## Output

A decision, not a catalogue. It leads with the recommended architecture and whether to retain, revise, or replace what you have, then covers product and constraints, current-state findings backed by repository evidence, component classification and topology, target architecture and state boundaries, safety and approval and tracing and evaluation design, plan gaps in order, decisions needing a named owner, and dated sources.

Checklist findings are **satisfied**, **partial**, **missing**, or **not applicable**. There is no single architecture score, because one number hides where the real problem is.

Sourced facts, repository observations, recommendations, assumptions, and unresolved decisions stay visibly separate. When the evidence genuinely cannot separate two options, it proposes a bounded spike with pass and fail criteria instead of picking one and sounding confident.

## What is in here

```
SKILL.md                                  entry point and review procedure
references/topology-decision.md           workflow vs agent vs multi-agent vs orchestrator
references/verification-and-evaluation.md whether autonomy and complexity are earned
references/knowledge-state-and-tools.md   durable knowledge, state, tools, graph decisions
references/adaptive-recovery.md           self-healing, reflection, cross-run learning
references/review-rubric.md               the full section-by-section rubric
evals/cases.json                          15 behavioural test cases
scripts/validate_skill.py                 fixture, navigation, and parity checks
```

References load on demand rather than all at once, so the context cost scales with what the review actually needs.

## Evals

`evals/cases.json` holds 15 behavioural cases covering the failure modes that matter: recommending a workflow where a supervisor plus one worker per fixed stage was proposed, allowing an orchestrator where the specialists genuinely cannot be known in advance, respecting a mandated multi-agent constraint, catching an implementation plan with no runtime quality work, not editing files when only feedback was asked for, not browsing when told not to, making a knowledge graph earn itself, refusing to answer "our baseline is inconsistent, so propose a multi-agent architecture" with an architecture instead of error analysis, capping a rubric-gated revision loop that chases zero partial marks, naming the runtime checkpointer a replacement service hand-rolled around, declining to add a workflow runtime to a job that reruns from scratch in a minute, and fixing context assembly before splitting one degrading agent into three.

Each case carries `expected_behaviors` and `forbidden_behaviors`. Run them with and without the skill, on each model and surface you care about. Forward tests only. Reading the cases is not running them.

```bash
python3 scripts/validate_skill.py
```

That checks the eval fixtures, the reference links in `SKILL.md`, and long-reference navigation. If you keep a matching copy under a sibling `.codex/skills/` it also enforces parity between them; with no mirror installed it prints a note and skips.

## License

MIT. See [LICENSE](LICENSE).
