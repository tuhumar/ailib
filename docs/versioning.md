# Versioning and release alignment

This document explains how to interpret versioning in the current public repository and how contributors should handle release/version changes while the project is still aligning repository truth with roadmap ambition.

---

## Current situation

The public repository exposes package metadata that already presents `ailib` as a mature versioned package.

At the same time, the roadmap and execution backlog explicitly include foundational work such as:

- repository truth alignment
- public API hardening
- protocol envelope consolidation
- CI and release-discipline tightening
- durable interruption / approval / resume semantics as future work

This means contributors should be careful not to treat version numbers alone as proof that every advanced roadmap capability is already complete.

---

## Policy during the alignment phase

Until the repository has completed the initial alignment milestones, use the following rules:

### 1. Repository truth beats aspiration

If there is any conflict between:

- code
- tests
- README
- changelog
- roadmap docs
- package version impression

then contributors should resolve the inconsistency explicitly instead of assuming the highest-maturity interpretation is correct.

### 2. Do not silently raise maturity claims

Do not merge changes that make the repository sound more advanced than the validated code/test/docs state.

Examples:

- do not describe roadmap-only capabilities as shipped
- do not imply durable replay/checkpoint/approval policy support unless it is implemented and documented together
- do not widen compatibility promises without tests and docs

### 3. Pair version-sensitive changes with docs updates

Any PR that materially changes one of these should update version/release docs in the same PR:

- public API contract
- protocol semantics
- compatibility guarantees
- packaging requirements
- CI/release behavior

---

## Practical release guidance

### Patch-level changes

Use patch-level changes for:

- bug fixes
- doc fixes that do not change behavior
- tests and CI hardening without public behavior changes
- non-breaking internal refactors

### Minor-level changes

Use minor-level changes for:

- additive capabilities that preserve the documented API contract
- new optional integrations or helpers
- new backends or protocol fields that are backward-compatible and clearly documented

### Major-level changes

Use major-level changes for:

- breaking public API changes
- incompatible protocol changes
- removal of supported legacy compatibility paths
- changes that alter expected integration behavior materially

---

## Recommended contributor habit

Before proposing a release-sensitive change, check all of the following together:

- `pyproject.toml`
- `README.md`
- `CHANGELOG.md`
- `docs/status.md`
- roadmap/backlog files when relevant

If they tell different stories, fix the story first or alongside the implementation.

---

## Long-term goal

Once the alignment phase is complete, `ailib` should move to a simpler release posture:

- public API stability is explicit
- protocol maturity is explicit
- roadmap capabilities are clearly separated from shipped behavior
- version numbers align cleanly with what users can actually rely on

Until then, contributors should optimize for **clarity and trust** over aggressive maturity signaling.
