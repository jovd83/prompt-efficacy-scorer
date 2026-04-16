# Sample Output: Already Strong DevOps Prompt

- Linked eval: `already-strong-devops-prompt`
- Eval ID: `1`

### Prompt Efficacy Scorecard: 92/100

| Dimension | Score | Why it matters | Findings |
| :-- | :-- | :-- | :-- |
| Intent preservation | 19/20 | Protects the user's actual objective | The request is specific and stable. |
| Instruction logic | 23/25 | Reduces contradictions and priority confusion | Constraints are compatible and ordered clearly. |
| Signal density | 18/20 | Removes dead weight and token waste | Nearly every line contributes directly to execution. |
| Structure | 18/20 | Improves readability and execution order | The prompt is concise and scannable. |
| Model/runtime fit | 14/15 | Aligns with context, tools, and execution environment | The output contract is appropriate for a code-generation workflow. |

### Critical Risks
- Minimal risk: the only notable improvement opportunity is slightly clearer formatting of the constraints.

### Recommended Strategy
- `stabilize`: the prompt is already strong and only needs a light-touch cleanup.

### Optimized Prompt
```markdown
Act as a Senior DevOps Engineer.

Generate a production-ready GitHub Actions workflow for a Node.js project.

Constraints:
- Use Node 20
- Include npm caching
- Trigger on push to main only

Output:
- Return only the YAML in a fenced code block
```

### Change Notes
- Kept: task, role, environment, and output constraints.
- Changed: normalized formatting to make the prompt easier to scan.
- Optional follow-up: none required unless the user wants deployment, matrix builds, or additional checks.

### Token / Complexity Impact
- Original length: short and efficient
- Revised length: roughly equivalent
- Expected impact: marginally better readability with no meaningful behavior change
