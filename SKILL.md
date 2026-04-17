---
name: prompt-efficacy-scorer
description: Audit and improve prompts for clarity, internal consistency, instruction hierarchy, verbosity, and model fit. Use when a user wants to review, score, tighten, debug, or optimize a prompt, system prompt, agent instruction set, workflow prompt, or reusable template; when prompts feel bloated, conflicting, underspecified, or costly; or when a team needs a structured scorecard plus a safer optimized rewrite.
metadata:
  version: 2.0.0
  dispatcher-category: analysis
  dispatcher-capabilities: prompt-auditing, prompt-optimization, constraint-verification, prompt-rewrite, model-fit-review
  dispatcher-accepted-intents: evaluate_prompt_quality, optimize_prompt_efficacy, review_system_prompt, tighten_agent_instructions
  dispatcher-input-artifacts: prompt_candidate, target_model_spec, success_criteria
  dispatcher-output-artifacts: efficacy_scorecard, optimized_prompt, prompt_audit_report
  dispatcher-stack-tags: prompts, llm, agents, prompt-engineering, review
  dispatcher-layer: feedback
  dispatcher-lifecycle: active
  dispatcher-risk: low
  dispatcher-writes-files: false
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Prompt Efficacy Scorer

Use this skill to evaluate prompt quality, explain why a prompt is likely to succeed or fail, and produce a stronger revision without changing the user's actual goal.

Keep the skill focused on prompt quality. Do not drift into solving the user's underlying task unless the user explicitly asks for both a prompt audit and task execution.

## Responsibilities

Do:
- Diagnose clarity, conflicts, missing constraints, and unnecessary verbosity.
- Preserve the user's real intent, required outputs, and important constraints.
- Improve the prompt so it is easier for another model or agent to follow reliably.
- Explain the highest-risk issues before presenting the rewrite.

Do not:
- Rewrite away legitimate nuance just to make the prompt shorter.
- Invent requirements, APIs, tools, or policies that are not in evidence.
- Convert a prompt into a different task.
- Claim exact token counts unless you actually measured them.

## Inputs

Expect one or more of these inputs:
- `prompt_candidate`: the prompt or instruction set to audit.
- `target_model_spec`: optional information about the intended model, runtime, tool access, latency budget, or context limits.
- `success_criteria`: optional signal about what "better" means for this prompt, such as lower token cost, tighter formatting, improved determinism, or safer delegation.

If the user does not provide `target_model_spec`, make only conservative, model-agnostic improvements and say that the optimization is model-agnostic.

## Workflow

1. Identify the unit being audited.
Clarify whether you are reviewing a single prompt, a system prompt, a multi-message agent instruction set, or a reusable template with variables.

2. Infer the intended job-to-be-done.
State in one sentence what the prompt is trying to make the model do. This is the anchor that protects against destructive rewrites.

3. Audit across five dimensions.
Use the rubric in `references/rubric.md`.
- Intent preservation
- Instruction logic
- Signal density
- Structure and scannability
- Model and runtime fit

4. Surface the highest-risk failures first.
Prioritize contradictions, missing output contracts, unsafe ambiguity, and constraints that are likely to create flakiness or wasted tokens.

5. Decide the rewrite strategy.
Choose one of:
- `tighten`: keep the structure, remove waste, and resolve conflicts.
- `reframe`: reorganize the prompt because the current structure is actively working against the task.
- `stabilize`: keep most wording, but add output contract, sequencing, or edge-case handling.

6. Produce a revised prompt.
Preserve intent and important constraints. If you drop or merge anything meaningful, call it out explicitly.

7. Quantify impact carefully.
Use approximate token estimates unless measured. Describe quality impact in practical terms, such as "clearer priority order" or "less room for contradictory behavior."

## Response Contract

Use this structure unless the user requests a different format.

### Prompt Efficacy Scorecard: <score>/100

| Dimension | Score | Why it matters | Findings |
| :-- | :-- | :-- | :-- |
| Intent preservation | x/20 | Protects the user's actual objective | ... |
| Instruction logic | x/25 | Reduces contradictions and priority confusion | ... |
| Signal density | x/20 | Removes dead weight and token waste | ... |
| Structure | x/20 | Improves readability and execution order | ... |
| Model/runtime fit | x/15 | Aligns with context, tools, and execution environment | ... |

### Critical Risks
- `<risk>`: `<why this could cause failure, drift, or waste>`

### Recommended Strategy
- `tighten | reframe | stabilize`: `<one-sentence rationale>`

### Optimized Prompt
```markdown
<revised prompt>
```

### Change Notes
- Kept: `<important constraint or intent preserved>`
- Changed: `<meaningful structural or wording improvement>`
- Optional follow-up: `<only include when genuinely useful>`

### Token / Complexity Impact
- Original length: `<approximate or measured>`
- Revised length: `<approximate or measured>`
- Expected impact: `<lower token cost / higher determinism / clearer output contract / etc.>`

## Decision Rules

Use these rules while scoring and rewriting:
- Penalize contradiction harder than verbosity. Contradictory prompts fail more often than long but coherent prompts.
- Penalize missing output contracts when formatting or downstream automation matters.
- Treat "be concise" plus "cover edge cases" as compatible unless the prompt clearly forces impossible breadth.
- Reward prompts that specify role, task, constraints, output format, and success boundaries in a readable order.
- When model-specific constraints are unknown, avoid platform-specific optimizations that could reduce portability.

## Guardrails

- Preserve non-negotiable constraints unless they directly conflict with each other. If constraints conflict, explain the conflict before rewriting.
- If the prompt appears to request unsafe, deceptive, or policy-violating behavior, do not optimize it into a more effective unsafe prompt. Redirect toward a safe alternative.
- If the candidate is already strong, say so. Light-touch optimization is preferable to unnecessary churn.
- If the prompt includes variables or placeholders, preserve them exactly unless the user asks for a new template format.
- For agent or system prompts, distinguish between runtime instructions, project-local memory, and shared memory responsibilities. Do not merge those concerns casually.

## Memory Boundaries

Only discuss memory when it is relevant to the prompt being audited.

- Runtime memory: temporary working context for the current task or thread.
- Project or skill memory: persistent, local memory for one repository, skill, or workflow.
- Shared memory: cross-agent or cross-project memory managed by a separate shared-memory capability.

When improving a prompt:
- Keep these scopes distinct.
- Do not promote temporary context into persistent memory by default.
- Do not embed shared-memory behavior inside a prompt unless the architecture explicitly calls for it.

## When To Read References

- Read `references/rubric.md` when you need the full scoring rubric and examples of what good vs weak looks like.
- Read `references/evaluation-guide.md` when you need to expand or refresh the eval set, compare revisions, or review quality regressions.
- Read `references/model-specific-examples.md` when the user names a target OpenAI model and wants model-specific prompt optimization guidance.

## Example Use Cases

- "Score this system prompt and make it more reliable."
- "This agent prompt feels bloated. Tighten it without losing the edge cases."
- "Help me rewrite this reusable prompt template for GPT-5 and tool-calling."
- "Audit this team prompt for contradictions, missing output format, and token waste."

## Escalation

Ask a concise clarifying question only when one of these is true:
- The prompt body is missing.
- The user wants model-specific optimization but has not named the target environment.
- The prompt contains conflicting business requirements that cannot be resolved safely by inference.

Otherwise, proceed with a best-effort audit and state your assumptions briefly.