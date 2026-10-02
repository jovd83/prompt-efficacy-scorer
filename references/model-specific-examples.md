# Model-Specific Guidance

Use this file when the user names a target model, vendor, or agent runtime and wants the audit tailored to it. Start with the vendor-neutral checks, then apply the matching vendor section.

These notes are deliberately short and practical. They are not a substitute for current vendor documentation, and model behavior changes between releases. When the user names a model released after the review dates below, say that the advice may be dated. Say explicitly which recommendations are model-specific, and don't state specs (context size, prices, rate limits) you haven't verified.

## Vendor-Neutral Checks

Apply these whatever the target:
- Untrusted input sits inside clear delimiters and is labeled as data, not instructions.
- Long documents or inputs come before the question or instructions that act on them.
- The output format is stated explicitly. If downstream code parses the output, the prompt says so and names the exact shape.
- Tools are scoped: what the model may read, change, run, or publish.
- Emphasis is used sparingly. Explaining why a rule matters works better than shouting it.

## OpenAI

Grounded in OpenAI API docs reviewed on April 16, 2026:
- GPT-5.2 usage guide: `https://platform.openai.com/docs/guides/latest-model`
- GPT-5.2 model page: `https://platform.openai.com/docs/models/gpt-5.2`
- GPT-5.2-Codex model page: `https://platform.openai.com/docs/models/gpt-5.2-codex`
- GPT-5 mini model page: `https://platform.openai.com/docs/models/gpt-5-mini`
- GPT-5 nano model page: `https://platform.openai.com/docs/models/gpt-5-nano`

Key doc-backed takeaways:
- `gpt-5.2` is positioned for complex reasoning, broad world knowledge, and multi-step agentic tasks.
- `gpt-5.2-codex` is optimized for long-horizon, agentic coding tasks.
- `gpt-5-mini` is a smaller cost-optimized reasoning/chat option.
- `gpt-5-nano` is positioned for high-throughput simpler instruction-following and classification work.

### `gpt-5.2`

Audit emphasis: preserve complex multi-step reasoning requirements; separate task, constraints, and output contract; reduce noise without flattening important context.

Good rewrite pattern: keep rich context when it changes the answer, make success criteria explicit, avoid over-compressing domain detail.

### `gpt-5.2-codex`

Audit emphasis: file-level or repository-level scope clarity; explicit expected artifacts such as code, tests, diffs, or reports; tool-use assumptions and coding boundaries.

Good rewrite pattern: separate coding task, acceptance checks, and safety constraints; state what should change and what must stay untouched; make output expectations concrete for coding workflows.

### `gpt-5-mini`

Audit emphasis: remove low-value verbosity, tighten the instruction hierarchy, prefer simple readable structure over prose-heavy framing.

Good rewrite pattern: short sections, an explicit output contract, fewer decorative personas and less repeated context. If one prompt asks for several large deliverables, recommend splitting them into separate calls.

### `gpt-5-nano`

Audit emphasis: extreme clarity, narrow task scope, highly constrained output formatting.

Good rewrite pattern: one job per prompt, minimal ambiguity, no complex synthesis expected from underspecified inputs.

## Anthropic Claude

Grounded in Anthropic's prompting best practices, reviewed on October 1, 2026:
- `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`

That page covers the current Claude models (including Opus 5.5, Sonnet 5.5, Haiku 4.5, and the Fable and Mythos families) and links per-model pages for differences such as effort calibration and response length. Check the per-model page when the user names a specific model.

Audit emphasis:
- **Precise instruction following.** Current Claude models do what the prompt says, so vague prompts get literal results. If the user wants "above and beyond" behavior, the prompt has to ask for it. "Suggest changes" and "make the changes" produce different behavior; check that the prompt says which it means.
- **Aggressive emphasis over-applies.** Anthropic notes these models are more responsive to the system prompt than earlier ones, and that language like "CRITICAL: You MUST use this tool when..." can cause overtriggering. Recommend normal phrasing ("Use this tool when..."), and remove leftover over-prompting such as "If in doubt, use X".
- **Explain the why.** Giving the reason behind an instruction helps Claude apply it in cases the prompt didn't list.
- **XML tags for structure.** Wrapping instructions, context, examples, and variable inputs in their own tags (`<instructions>`, `<context>`, `<input>`) reduces misreading. This is also the natural boundary for untrusted input.
- **Long documents first.** Put long inputs near the top and the question or instructions at the end.
- **Output format without prefill.** Anthropic documents moving away from prefilled assistant turns. For format control, recommend direct instructions, XML output tags, structured outputs, or tool calls.

Agent harnesses (Claude Code, the Agent SDK, and similar):
- Check whether the prompt replaces the harness's default system prompt or is added to it. Replacing it can drop the harness's built-in guidance on tools and safety.
- Scope the tools: read-only or not, which commands may run, and whether the agent may commit, push, or post.
- Stateless runs can't know things like "this is the first review" unless the input says so. Flag rules that depend on state the agent doesn't have.

## Google Gemini

Grounded in Google's "Prompt design strategies" page for the Gemini API, reviewed on October 1, 2026:
- `https://ai.google.dev/gemini-api/docs/prompting-strategies`

Audit emphasis:
- **Clear, specific instructions.** For Gemini 3, the guidance is to be precise and direct and to state the goal concisely.
- **Few-shot examples.** Google recommends always including few-shot examples, with consistent formatting across them. A prompt for a format-sensitive task with no examples is a gap worth flagging. Recommend that the user add examples drawn from their real data; don't invent them in the rewrite.
- **Context first, question last.** For long context, supply all the context first and put the specific instruction or question at the very end.
- **Structure.** XML tags or Markdown headings, used consistently.
- **Verbosity.** Gemini 3 models default to direct, efficient answers. If the user needs depth, the prompt has to ask for it.
- **Sampling settings.** Google recommends leaving temperature and related settings at their defaults for Gemini 3.x models. Mention this only if the user controls those parameters.

## Other Vendors

Apply the vendor-neutral checks, say that the advice is not vendor-specific, and suggest checking the vendor's current prompting guide.
