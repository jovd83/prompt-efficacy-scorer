# Prompt Audit Rubric

Use this rubric when scoring prompts with `prompt-efficacy-scorer`.

## Scoring Philosophy

The score should predict practical execution quality, not just writing style. A shorter prompt is not automatically better. A longer prompt can still score well if it is coherent, necessary, and easy to follow.

Total score: `100`

## 1. Intent Preservation `0-20`

Question: does the prompt communicate a stable, recognizable objective?

Strong signs:
- clear task objective
- stable audience or role
- no accidental drift into adjacent tasks
- important requirements are explicit

Weak signs:
- vague job-to-be-done
- mixed objectives without priority
- implied but unstated success conditions

## 2. Instruction Logic `0-25`

Question: are the instructions internally compatible and prioritized well?

Strong signs:
- no contradictions
- clear priority order
- compatible constraints
- explicit tradeoffs when needed

Weak signs:
- "be brief" and "explain in extreme detail" with no hierarchy
- conflicting output instructions
- impossible combinations of speed, depth, and format

## 3. Signal Density `0-20`

Question: how much of the prompt materially helps execution?

Strong signs:
- most lines steer behavior
- little filler or roleplay clutter
- examples or context justify their token cost

Weak signs:
- repeated statements
- decorative persona language with no operational value
- unnecessary backstory that does not change the task

## 4. Structure and Scannability `0-20`

Question: can a model or human quickly identify the task, constraints, and output contract?

Strong signs:
- logical ordering
- readable formatting
- separate task, constraints, and output sections
- explicit delimiters where useful

Weak signs:
- one dense paragraph with many rules
- output format hidden inside prose
- edge cases mixed into the main task without grouping

## 5. Model / Runtime Fit `0-15`

Question: does the prompt fit the actual execution environment?

Strong signs:
- realistic expectations for the target model and tools
- explicit tool or context assumptions
- formatting and reasoning expectations that match the runtime

Weak signs:
- requests that assume tools the model does not have
- excessive prompt length for a tight context budget
- hidden dependency on shared memory or persistent state

## Rewrite Strategy Heuristics

Choose `tighten` when:
- the structure is mostly sound
- the prompt is just wordy or repetitive
- only light conflict resolution is needed

Choose `reframe` when:
- the prompt mixes multiple responsibilities
- the task, constraints, and output are tangled together
- the ordering makes good execution unlikely

Choose `stabilize` when:
- the prompt is mostly good
- it needs clearer output boundaries, sequencing, or failure handling
- you want minimal change with better reliability

## Examples

### Weak

```text
Act like the world's best architect, coder, growth hacker, and PM. Be concise and exhaustive. Give me only bullet points and also a full essay. Keep it under 100 words but cover all edge cases.
```

Likely outcome:
- low instruction logic
- low structure
- moderate signal density at best

### Strong

```text
Act as a backend reviewer. Review the API proposal below for breaking changes.

Output:
1. Breaking changes
2. Migration risks
3. Recommended fixes

Constraints:
- Focus on compatibility and rollout risk
- Be concise
- Do not redesign unrelated parts of the system
```

Likely outcome:
- high intent preservation
- high instruction logic
- strong structure

## Scoring Discipline

- Do not inflate scores just because the topic is sophisticated.
- Do not over-penalize prompts that are detailed for legitimate reasons.
- If the prompt is already strong, say that the improvement is marginal rather than forcing a dramatic rewrite.
