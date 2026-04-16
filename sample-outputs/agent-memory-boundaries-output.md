# Sample Output: Agent Prompt With Memory Boundaries

- Linked eval: `agent-prompt-with-memory-boundaries`
- Eval ID: `3`

### Prompt Efficacy Scorecard: 28/100

| Dimension | Score | Why it matters | Findings |
| :-- | :-- | :-- | :-- |
| Intent preservation | 10/20 | Protects the user's actual objective | The roadmap request is clear, but the memory behavior is unsafe and underspecified. |
| Instruction logic | 5/25 | Reduces contradictions and priority confusion | Temporary notes are being treated as permanent shared memory without review. |
| Signal density | 5/20 | Removes dead weight and token waste | Several instructions encourage unsafe invention rather than reliable execution. |
| Structure | 4/20 | Improves readability and execution order | Execution goals and memory policies are mixed together. |
| Model/runtime fit | 4/15 | Aligns with context, tools, and execution environment | The prompt assumes durable cross-agent memory without defining the system boundary. |

### Critical Risks
- Unsafe memory promotion: runtime context is being promoted into persistent and shared memory automatically.
- Fabricated facts: the instruction to invent project facts undermines trust and auditability.

### Recommended Strategy
- `reframe`: the prompt needs explicit memory boundaries and a safer failure mode.

### Optimized Prompt
```markdown
Act as a project planning agent.

Task:
Produce a roadmap for the project based only on information provided in the current conversation and any explicitly supplied project documents.

Memory boundaries:
- Treat notes from the current thread as runtime working context only.
- Do not store runtime notes as persistent project memory unless a separate project-memory process explicitly requests it.
- Do not publish information to shared memory unless an external shared-memory workflow approves the promotion.

Safety:
- If important facts are missing, call them out as assumptions or open questions.
- Do not invent project facts to keep the plan moving.

Output:
- Provide sections for confirmed facts, open assumptions, roadmap, and recommended next actions.
```

### Change Notes
- Kept: the request for a project roadmap.
- Changed: separated runtime concerns from persistent memory and removed the instruction to invent facts.
- Optional follow-up: connect the workflow to a dedicated shared-memory capability if durable promotion is truly needed.

### Token / Complexity Impact
- Original length: short but unsafe and ambiguous
- Revised length: longer, but much more auditable
- Expected impact: safer execution, cleaner architecture boundaries, and fewer hallucinated project assumptions
