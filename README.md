# Prompt Efficacy Scorer

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Validation](https://img.shields.io/badge/validation-executable-success)

`prompt-efficacy-scorer` is an AgentSkill for auditing prompts and producing safer, clearer, lower-waste rewrites. It is designed for teams who want a repeatable way to review prompts for contradiction, ambiguity, poor structure, missing output contracts, and weak model/runtime fit.

The skill is intentionally narrow: it improves prompts. It does not automatically execute the task described by the prompt, and it does not try to become a full prompt-management platform.

## What This Skill Is Responsible For

- Scoring prompt quality using a structured rubric
- Explaining the most important prompt risks in plain language
- Producing an optimized revision that preserves intent
- Distinguishing between light cleanup and deeper restructuring
- Handling prompts that include agent instructions, templates, or memory-related language

## What This Repository Is Not

- Not a general-purpose agent framework
- Not a shared-memory implementation
- Not an autonomous self-improving prompt system
- Not a benchmark suite for every model vendor

Optional integrations such as dispatch logging, external benchmark viewers, or shared-memory infrastructure should remain architectural boundaries around the skill rather than being embedded into the core prompt-auditing logic.

## Repository Layout

```text
prompt-efficacy-scorer/
|-- LICENSE
|-- SKILL.md
|-- README.md
|-- VERSION
|-- agents/
|   `-- openai.yaml
|-- evals/
|   `-- evals.json
|-- sample-outputs/
|   |-- contradictory-code-generation-output.md
|   |-- already-strong-devops-output.md
|   `-- agent-memory-boundaries-output.md
|-- scripts/
|   `-- validate_skill.py
`-- references/
    |-- rubric.md
    |-- evaluation-guide.md
    `-- model-specific-examples.md
```

Current version: `2.1.0`

License: `MIT`

## Install

Place this folder in your AgentSkill directory so your agent runtime can discover it.

Common locations:
- `~/.agents/skills/prompt-efficacy-scorer`
- `~/.codex/skills/prompt-efficacy-scorer`

The required file is `SKILL.md`. The other files improve usability, evaluation, and UI metadata.

## When To Use It

Use this skill when a user asks to:
- score or audit a prompt
- rewrite a prompt without changing intent
- reduce prompt bloat or token waste
- debug conflicting instructions
- improve a system prompt, agent prompt, or reusable template
- tighten output contracts for automation or team reuse

## Expected Inputs

- `prompt_candidate`: required prompt or instruction set to review
- `target_model_spec`: optional target environment details such as model family, tool access, context limits, or latency constraints
- `success_criteria`: optional optimization goal such as lower cost, higher determinism, stronger formatting, or safer delegation

## Expected Output

The default output is:
- a short header: what was audited, the prompt's job in one sentence, any assumptions, and a one-line verdict
- a numeric scorecard, scored against fixed anchors so repeat runs land close together
- a small set of critical risks
- a rewrite strategy: `tighten`, `reframe`, `stabilize`, or `scaffold` (for prompts too thin to run reliably)
- an optimized prompt
- a short change log that separates what was kept, what was changed, and what was added as an assumption for you to confirm
- an approximate complexity or token impact statement

## Design Principles

- Preserve intent before optimizing wording.
- Penalize contradictions more heavily than length.
- Leave strong prompts mostly alone, and say so.
- Label every default the rewrite adds instead of passing it off as the user's requirement.
- Treat content the prompt's author doesn't control (tickets, documents, PR text) as data, never as instructions.
- Prefer auditable improvements over vague "better prompt" claims.
- Keep runtime memory, project-local memory, and shared memory separate.
- Stay model-agnostic unless the user supplies model-specific constraints.

## Evaluation Strategy

The eval set is in [evals/evals.json](./evals/evals.json). Each eval has a list of `expectations` to grade against. It covers:
- contradictory prompts
- already-good prompts
- underspecified prompts
- structured agent prompts with memory boundaries
- prompts where shortening too aggressively would remove necessary nuance
- a model-specific prompt for an OpenAI model
- a template with placeholders whose output is parsed as JSON
- a tool-using agent prompt for a Claude model that reads untrusted PR content

See [references/evaluation-guide.md](./references/evaluation-guide.md) for how to extend the eval suite and compare revisions.

Sample record outputs are checked in under [sample-outputs/](./sample-outputs/) so reviewers can quickly inspect what good skill behavior looks like without running a full benchmark stack.
Each sample output includes its linked `eval_name` and `eval_id` for traceability back to [evals/evals.json](./evals/evals.json).

## Executable Validation

This repository now includes an executable validation script:

```bash
python scripts/validate_skill.py
```

It verifies:
- required repository files exist
- `evals/evals.json` parses correctly
- the README mentions the current version and MIT license
- UI metadata is present
- every eval has at least one expectation
- sample outputs exist
- the model-specific guidance covers the documented OpenAI model variants and has Anthropic Claude and Google Gemini sections

This is intentionally lightweight validation, not a full benchmark harness.

## Model-Specific Examples

The skill itself remains model-agnostic by default. When the user names a target model, vendor, or agent runtime, [references/model-specific-examples.md](./references/model-specific-examples.md) shows how to adapt the audit. It starts with vendor-neutral checks, then covers:
- OpenAI: `gpt-5.2` for complex reasoning and multi-step agentic tasks, `gpt-5.2-codex` for long-horizon coding workflows, `gpt-5-mini` for cost-optimized reasoning/chat, and `gpt-5-nano` for high-throughput simpler instruction-following tasks
- Anthropic Claude: literal instruction following, toned-down emphasis, XML-tagged inputs, and agent-harness concerns such as tool scope
- Google Gemini: few-shot examples, context before the question, and Gemini 3 defaults

Each vendor section names its source and the date it was reviewed.

## GitHub Readiness Notes

This repository is meant to be publishable as a focused, reusable skill:
- `SKILL.md` stays concise and operational
- reference material lives in `references/`
- evaluation artifacts live in `evals/`
- UI metadata lives in `agents/openai.yaml`

## Suggested Future Extensions

These are deliberately out of scope for the current repository:
- measured token accounting via a tokenizer utility
- a dedicated benchmark runner script
- model-specific companion references
- shared-memory integration examples

If you add these later, keep them optional and preserve the skill's narrow core responsibility.
