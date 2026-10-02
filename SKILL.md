---
name: prompt-efficacy-scorer
description: Audit and improve prompts for clarity, consistency, instruction hierarchy, verbosity, and model fit. Use to review, score, tighten, debug, or optimize a prompt, system prompt, agent instructions, or template, or deliver a scorecard plus an optimized rewrite.
metadata:
  author: jovd83
  version: 2.1.0
---

# Prompt Efficacy Scorer

> **Version:** 2.1.0


Use this skill to evaluate prompt quality, explain why a prompt is likely to succeed or fail, and produce a stronger revision without changing the user's actual goal.

Keep the skill focused on prompt quality. Do not drift into solving the user's underlying task unless the user explicitly asks for both a prompt audit and task execution.

## Responsibilities

Do:
- Diagnose clarity, conflicts, missing constraints, unprotected inputs, and unnecessary verbosity.
- Preserve the user's real intent, required outputs, and important constraints.
- Improve the prompt so it is easier for another model or agent to follow reliably.
- Explain the highest-risk issues before presenting the rewrite.

Do not:
- Rewrite away legitimate nuance just to make the prompt shorter.
- Present anything you added as if the user had asked for it (see Filling Gaps).
- Invent facts about the user's product, data, tools, or environment.
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
State in one sentence what the prompt is trying to make the model do. This is the anchor that protects against destructive rewrites, and it goes in the response header so the user can correct it.

3. Audit across five dimensions.
Read `references/rubric.md` before scoring. Its anchors keep the same prompt from getting a different score on every run.
- Intent preservation
- Instruction logic
- Signal density
- Structure and scannability
- Model and runtime fit

4. Surface the highest-risk failures first.
Prioritize contradictions, constraints that force misleading output, missing output contracts, untrusted input without boundaries, and ambiguity that will make results flaky or wasteful.

5. Decide the rewrite strategy.
Choose one of:
- `tighten`: keep the structure, remove waste, and resolve conflicts.
- `reframe`: reorganize the prompt because the current structure is actively working against the task.
- `stabilize`: keep most wording, but add output contract, sequencing, or edge-case handling.
- `scaffold`: the prompt is too thin to run reliably; build the missing input slots, scope, and output contract around the user's goal.

If two strategies fit, pick the one that changes less.

6. Produce a revised prompt.
Preserve intent and important constraints. Anything you drop, merge, or add goes in Change Notes.

7. Quantify impact carefully.
Use approximate token estimates unless measured. Describe quality impact in practical terms, such as "clearer priority order" or "less room for contradictory behavior."

## Response Contract

Use this structure unless the user requests a different format.

**Audited:** `<unit>` (`<target model/runtime, or "model-agnostic">`)
**Job:** `<one sentence: what the prompt is trying to make the model do>`
**Assumptions:** `<only those that affect the audit; omit the line if there are none>`
**Verdict:** `<strong | workable | weak | broken>`: `<the main reason, in one or two sentences>`

### Prompt Efficacy Scorecard: <score>/100

| Dimension | Score | Why it matters | Findings |
| :-- | :-- | :-- | :-- |
| Intent preservation | x/20 | Protects the user's actual objective | ... |
| Instruction logic | x/25 | Reduces contradictions and priority confusion | ... |
| Signal density | x/20 | Removes dead weight and token waste | ... |
| Structure | x/20 | Improves readability and execution order | ... |
| Model/runtime fit | x/15 | Aligns with context, tools, inputs, and execution environment | ... |

### Critical Risks
- `<risk>`: `<why this could cause failure, drift, or waste>`

If nothing is critical, say so in one line and list the top risks with their severity (`moderate` or `minor`).

### Recommended Strategy
- `tighten | reframe | stabilize | scaffold`: `<one-sentence rationale>`

### Optimized Prompt
```markdown
<revised prompt>
```

If the revised prompt itself contains code fences, wrap it in a four-backtick fence so it renders as one block.

### Change Notes
- Kept: `<important constraint or intent preserved>`
- Changed: `<meaningful structural or wording improvement, and which risk it fixes>`
- Added (assumption): `<a default you introduced; the user should confirm or replace it>`
- Optional follow-up: `<only when genuinely useful>`

When the prompt will be reused, automated, or drive an agent, use the follow-up to suggest one cheap check: run the rewrite on three to five representative inputs, including an edge case and one input that should produce an empty or "no issues" result.

### Token / Complexity Impact
- Original length: `<approximate or measured>`
- Revised length: `<approximate or measured>`
- Expected impact: `<lower token cost / higher determinism / clearer output contract / etc.>`

## Decision Rules

Use these rules while scoring and rewriting:
- Penalize contradiction harder than verbosity. Contradictory prompts fail more often than long but coherent prompts.
- Penalize missing output contracts when formatting or downstream automation matters.
- Treat "be concise" plus "cover edge cases" as compatible unless the requested breadth cannot fit the requested length. When it cannot, name the conflict.
- Treat a constraint that forces misleading output as a conflict with accuracy. Examples: a quota of findings ("always find at least 5 issues"), "never say you don't know", "assume missing facts". The user almost always wanted thoroughness, not padding. Explain the conflict, replace the constraint with its honest version, and flag the departure in Change Notes.
- When two instructions conflict, resolve toward the one that best fits the job-to-be-done and say which side you chose. If the other reading is just as plausible and would change the deliverable, offer it as a one-line alternative under Optional follow-up. Don't stop the audit to ask; Escalation lists the only reasons to ask first.
- Check every input the prompt's author does not control: user messages, tickets, documents, PR text, web pages, tool output. It should be delimited and labeled as data, not as instructions. If the model has tools or its output feeds automation, missing boundaries is a Critical Risk, because that content can carry instructions of its own. Otherwise, list it as a moderate risk.
- For tool-using agents, check scope: what the agent may read, change, run, or publish. Granting tools without boundaries costs points on runtime fit.
- Reward prompts that specify role, task, constraints, output format, and success boundaries in a readable order.
- When model-specific constraints are unknown, avoid platform-specific optimizations that could reduce portability.

## Filling Gaps

Weak prompts often lack something a reliable prompt needs, such as JSON keys, enum values, a priority scale, a scope limit, or what "production-ready" means. Leaving the gap keeps the prompt flaky. Silently filling it changes what the user asked for. Do this instead:
- For structure and conventions, propose a concrete default and list it under "Added (assumption)" so the user can confirm or replace it.
- For facts only the user knows, such as their product, data, audience, or repo layout, add a placeholder instead of guessing. Match the template syntax the prompt already uses (`{{var}}`, `<var>`, `$VAR`); if it uses none, use `{{double_braces}}`, which can't be confused with XML tags.
- Name every new placeholder or delimiter in Change Notes.

## Guardrails

- Preserve non-negotiable constraints unless they conflict with each other or with accuracy (see Decision Rules). If you change one, explain why before the rewrite.
- If the prompt appears to request unsafe, deceptive, or policy-violating behavior, do not optimize it into a more effective unsafe prompt. Redirect toward a safe alternative.
- If the candidate is already strong (80 or more), say so plainly and keep the original wording and order unless a named risk, including a model-specific one, requires a change. Every addition should trace to a named risk. Problems outside the prompt's wording, such as an outdated version number or a deprecated API it names, belong in Optional follow-up, not in silent edits to the user's constraints.
- Whatever the strategy, if the rewrite grows beyond about twice the original length, say why under Token / Complexity Impact. `scaffold` and `reframe` rewrites often need that room; for a strong prompt it usually means you are over-editing, so cut back.
- If the prompt includes variables or placeholders, preserve them exactly unless the user asks for a new template format.
- For agent or system prompts, distinguish between runtime instructions, project-local memory, and shared memory responsibilities. Do not merge those concerns casually.

## Memory Boundaries

Only discuss memory when it is relevant to the prompt being audited.

- Runtime memory: temporary working context for the current task or thread.
- Project or skill memory: persistent, local memory for one repository, skill, or workflow.
- Shared memory: cross-agent or cross-project memory managed by a separate shared-memory capability.

When improving a prompt:
- Keep these scopes distinct.
- Nothing moves from runtime into project or shared memory without an explicit trigger: the user's approval or a named process the prompt identifies. "Save confirmed facts" is not a trigger unless the prompt says who confirms.
- Do not embed shared-memory behavior inside a prompt unless the architecture explicitly calls for it.
- Tell the agent not to report that something was saved unless the save actually happened.

## When To Read References

- Read `references/rubric.md` before scoring. It has the score anchors, the dimension definitions, and examples of what good and weak look like.
- Read `references/model-specific-examples.md` when the user names a target model, vendor, or agent runtime (OpenAI, Anthropic Claude, Google Gemini, Claude Code, or another) and wants the audit tailored to it.
- Read `references/evaluation-guide.md` when you need to expand or refresh the eval set, compare revisions, or review quality regressions.

## Example Use Cases

- "Score this system prompt and make it more reliable."
- "This agent prompt feels bloated. Tighten it without losing the edge cases."
- "Help me rewrite this reusable prompt template for GPT-5 and tool-calling."
- "Review the system prompt for our Claude code-review agent."
- "Audit this team prompt for contradictions, missing output format, and token waste."

## Escalation

Ask a concise clarifying question only when one of these is true:
- The prompt body is missing.
- The user wants model-specific optimization but has not named the target environment.
- The prompt contains conflicting business requirements that cannot be resolved safely by inference.

Otherwise, proceed with a best-effort audit and state your assumptions briefly in the header.
