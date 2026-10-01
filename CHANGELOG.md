# Changelog

All notable changes to this repository are documented here.

## [2.0.2] - 2026-10-01

### Changed
- `metadata` carries `author` and `version`, as the other skills in this library do.
- Every version marker says 2.0.2. They disagreed before (README badge 2.0.0); this release continues from the highest.

### Removed
- The `dispatcher-*` routing keys from the SKILL.md metadata. Nothing reads them since skill-dispatcher 5.0.0, which builds its registry from names and descriptions.

## [2.0.1] - 2026-04-30

### Changed
- Trim `SKILL.md` frontmatter to fit the 1000-character dispatcher limit (description trim, migrate non-dispatcher fields to body).

