# Versioning and release alignment

This document explains how to interpret versioning in the current public repository and how contributors should handle release/version changes while the project is still aligning repository truth with roadmap ambition.

## Current situation

The public repository exposes package metadata that already presents `ailib` as a mature versioned package.

At the same time, the roadmap and execution backlog explicitly include foundational work such as repository truth alignment, public API hardening, protocol envelope consolidation, CI tightening, and durable interruption/approval/resume semantics as future work.

This means contributors should be careful not to treat version numbers alone as proof that every advanced roadmap capability is already complete.

## Policy during the alignment phase

### 1. Repository truth beats aspiration
If there is any conflict between code, tests, README, changelog, roadmap docs, and package version impression, contributors should resolve the inconsistency explicitly instead of assuming the highest-maturity interpretation is correct.

### 2. Do not silently raise maturity claims
Do not merge changes that make the repository sound more advanced than the validated code/test/docs state.

### 3. Pair version-sensitive changes with docs updates
Any PR that materially changes public API, protocol semantics, compatibility guarantees, packaging requirements, or CI/release behavior should update version/release docs in the same PR.

## Practical release guidance

### Patch-level changes
- bug fixes
- doc fixes that do not change behavior
- tests and CI hardening without public behavior changes
- non-breaking internal refactors

### Minor-level changes
- additive capabilities that preserve the documented API contract
- new optional integrations or helpers
- new backends or protocol fields that are backward-compatible and clearly documented

### Major-level changes
- breaking public API changes
- incompatible protocol changes
- removal of supported legacy compatibility paths
- changes that alter expected integration behavior materially

## Recommended contributor habit
Before proposing a release-sensitive change, check `pyproject.toml`, `README.md`, `CHANGELOG.md`, `docs/status.md`, and the roadmap/backlog files together. If they tell different stories, fix the story first or alongside the implementation.

## Long-term goal
Once the alignment phase is complete, `ailib` should move to a simpler release posture:
- public API stability is explicit
- protocol maturity is explicit
- roadmap capabilities are clearly separated from shipped behavior
- version numbers align cleanly with what users can actually rely on

Until then, contributors should optimize for clarity and trust over aggressive maturity signaling.
