# Changelog

All notable changes to this repository are documented here.

## [2.1.0] - 2026-10-02

### Added
- A response header (audited unit, job-to-be-done, assumptions, verdict). Workflow steps 1-2 asked for these, but the response contract had no place for them.
- A `scaffold` rewrite strategy for prompts too thin to run reliably, and a tie-break: when two strategies fit, pick the one that changes less.
- A "Filling Gaps" section: propose concrete defaults labeled as assumptions, and use placeholders only for facts only the user knows.
- Decision rules for constraints that force misleading output (finding quotas, "assume missing facts"), for resolving conflicts, for untrusted input, and for tool scope.
- Score anchors and overall score bands in `references/rubric.md`, plus untrusted-input and tool-scope signs under model/runtime fit.
- Anthropic Claude and Google Gemini sections, and vendor-neutral checks, in `references/model-specific-examples.md`, each with its source and review date.
- Four evals: a JSON-pipeline template with placeholders, a Claude Code review agent that reads untrusted PR content, a Gemini HR-policy RAG template, and an already-strong Claude meeting-summary prompt.
- `expectations` for every eval, and a validator check that each eval has them.

### Changed
- "Already strong" now has a measurable bar: keep wording and order, trace every addition to a named risk, and explain any rewrite that grows past about twice the original length.
- Memory boundaries: nothing moves into project or shared memory without an explicit trigger, and "confirmed" alone does not count.
- Conflicts no longer pause the audit for a question: the skill picks the likelier reading and offers the other as a one-line alternative.
- New placeholders default to `{{double_braces}}`, so they can't be confused with XML tags in Claude-targeted rewrites.
- Critical Risks may say "nothing critical" and list moderate or minor risks instead.
- Sample outputs show the new header, and the contradictory-prompt sample says which side of each conflict it chose.
- `references/evaluation-guide.md` explains how to write expectations that tell a skill run apart from a run without the skill.

### Fixed
- README said "Current version: 2.0.0" and had a broken layout tree.

## [2.0.2] - 2026-10-01

### Changed
- `metadata` carries `author` and `version`, as the other skills in this library do.
- Every version marker says 2.0.2. They disagreed before (README badge 2.0.0); this release continues from the highest.

### Removed
- The `dispatcher-*` routing keys from the SKILL.md metadata. Nothing reads them since skill-dispatcher 5.0.0, which builds its registry from names and descriptions.

## [2.0.1] - 2026-04-30

### Changed
- Trim `SKILL.md` frontmatter to fit the 1000-character dispatcher limit (description trim, migrate non-dispatcher fields to body).

