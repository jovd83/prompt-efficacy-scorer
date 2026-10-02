# Sample Output: Contradictory Code Generation Prompt

- Linked eval: `contradictory-code-generation-prompt`
- Eval ID: `0`

**Audited:** a single code-generation prompt, model-agnostic
**Job:** get a Python function that computes the Fibonacci sequence, with some explanation of how it works.
**Verdict:** broken: four pairs of instructions contradict each other, so any output will ignore part of the prompt.

### Prompt Efficacy Scorecard: 34/100

| Dimension | Score | Why it matters | Findings |
| :-- | :-- | :-- | :-- |
| Intent preservation | 12/20 | Protects the user's actual objective | The core task is visible, but secondary instructions distort it. |
| Instruction logic | 4/25 | Reduces contradictions and priority confusion | "Stay brief" conflicts with "explain every line in depth"; "add comments" conflicts with "do not use comments." |
| Signal density | 6/20 | Removes dead weight and token waste | Several clauses add noise without improving the request. |
| Structure | 7/20 | Improves readability and execution order | Constraints are buried inside one dense paragraph. |
| Model/runtime fit | 5/15 | Aligns with context, tools, and execution environment | The prompt asks for incompatible tradeoffs rather than a realistic coding brief. |

### Critical Risks
- Constraint collision: the model may satisfy only a subset of the prompt and ignore the rest.
- Low determinism: multiple incompatible instructions create unstable outputs.

### Recommended Strategy
- `reframe`: the prompt needs a coherent task/constraint/output structure rather than small wording cleanup.

### Optimized Prompt
```markdown
Act as a Python engineer.

Task:
Implement a Fibonacci sequence function in Python using only the standard library.

Constraints:
- Prefer an efficient implementation.
- Include brief docstrings or short inline comments only if they clarify the approach.
- Do not include Java-specific guidance unless explicitly requested.

Output:
- Return one Python code block only.
```

### Change Notes
- Kept: the core request to generate a Python Fibonacci implementation, standard library only.
- Changed: "very efficient" won over "recursion without memoization", because naive recursion is exponential and the prompt calls efficiency a requirement.
- Changed: "stay brief" won over "explain every line in depth", and the one-code-block output replaces "no commentary".
- Changed: "DO NOT USE COMMENTS" (the last and most emphatic rule) was softened to "only if they clarify the approach". The Java comments were dropped because the Java port is hypothetical.
- Changed: reorganized the prompt into task, constraints, and output sections.
- Optional follow-up: if the user wants a teaching version, ask whether they prefer explanation or production efficiency; that choice flips two of the decisions above.

### Token / Complexity Impact
- Original length: approximate medium-length prompt with high internal conflict
- Revised length: shorter and more stable
- Expected impact: higher determinism and less wasted reasoning on contradictory priorities
