# Model-Specific Examples

This file contains concrete examples for adapting prompt audits when the user provides a target OpenAI model or runtime profile.

These examples are intentionally narrow and practical. They are not meant to replace current OpenAI documentation. Re-check current docs when model guidance changes.

## Source Notes

The examples below are grounded in current OpenAI API docs reviewed on April 16, 2026:
- GPT-5.2 usage guide: `https://platform.openai.com/docs/guides/latest-model`
- GPT-5.2 model page: `https://platform.openai.com/docs/models/gpt-5.2`
- GPT-5.2-Codex model page: `https://platform.openai.com/docs/models/gpt-5.2-codex`
- GPT-5 mini model page: `https://platform.openai.com/docs/models/gpt-5-mini`
- GPT-5 nano model page: `https://platform.openai.com/docs/models/gpt-5-nano`

Key doc-backed takeaways used here:
- `gpt-5.2` is positioned for complex reasoning, broad world knowledge, and multi-step agentic tasks.
- `gpt-5.2-codex` is optimized for long-horizon, agentic coding tasks.
- `gpt-5-mini` is a smaller cost-optimized reasoning/chat option.
- `gpt-5-nano` is positioned for high-throughput simpler instruction-following and classification work.

## Example 1: `gpt-5.2`

Use when the prompt targets a strong general-purpose reasoning model.

Audit emphasis:
- preserve complex multi-step reasoning requirements
- ensure the task, constraints, and output contract are clearly separated
- reduce noise without flattening important context

Good rewrite pattern:
- keep rich context when it changes the answer
- make success criteria explicit
- avoid over-compressing domain detail

## Example 2: `gpt-5.2-codex`

Use when the prompt targets agentic coding work.

Audit emphasis:
- file-level or repository-level scope clarity
- explicit expected artifacts such as code, tests, diffs, or reports
- tool-use assumptions and coding boundaries

Good rewrite pattern:
- separate coding task, acceptance checks, and safety constraints
- state what should be changed versus what must remain untouched
- make output expectations concrete for coding workflows

## Example 3: `gpt-5-mini`

Use when the prompt targets a cost-optimized model and still needs good reasoning.

Audit emphasis:
- remove low-value verbosity
- tighten instruction hierarchy
- prefer simple, readable structure over prose-heavy framing

Good rewrite pattern:
- short sections
- explicit output contract
- fewer decorative personas and less repeated context

## Example 4: `gpt-5-nano`

Use when the prompt targets high-throughput, simpler instruction-following tasks.

Audit emphasis:
- extreme clarity
- narrow task scope
- highly constrained output formatting

Good rewrite pattern:
- one job per prompt
- minimal ambiguity
- avoid expecting complex synthesis from underspecified inputs

## Operational Guidance

When a user names a target model:
- tailor the audit to that model's expected role and cost/performance profile
- keep the rewrite faithful to the user's actual goal
- say explicitly when the optimization advice is model-specific

When a user does not name a target model:
- keep the audit model-agnostic
- avoid advice that depends on a specific API or model family
