---
type: framework
themes:
  - repository-architecture
  - knowledge-management
confidence: medium
reuse:
  - blog
  - book
  - consulting
source: chat
tags:
  - repository
  - architecture
  - git
  - knowledge-os
  - multi-layer-system
---

# How to Split Repositories

## Claim
A multi-layer book system works best when the semantic layer (knowledge) and the production layer (pipeline) are stored in different repositories.

## Why it matters
Keeping blocks, invariants, and decision logs in the same Git history as drafts and pipeline scripts leads to:
- Noise in commit history
- Accidental exposure of internal reasoning
- Merge conflicts
- Loss of semantic stability

Separation allows each layer to evolve independently and protects the meaning layer from accidental modification.

## Models (valid architectures)

### 1. Dual-Repo Split (recommended)
- Repo A: **pipeline + chapters + tools**
- Repo B: **knowledge/** (blocks, invariants, map, decisions)
- Both repos live locally; pipeline reads B as external source.
- Best for: privacy, composability, multi-book knowledge reuse.

### 2. Submodule Split
- Repo A (main): pipeline, chapters.
- Repo B: knowledge.
- B is added into A via git submodule.
- Best for: versioned knowledge dependencies, single checkout workflow.

### 3. Monorepo with Strict Separation
- Single repo with strict directory boundaries:
  - `knowledge/` (read-only for pipeline)
  - `pipeline/` (production layer)
  - `chapters/` (output)
- Enforced via tooling/scripts.
- Best for: simplicity, single source of truth, when privacy is not a concern.

## Decision criteria

Choose Dual-Repo Split if:
- Knowledge needs to be private
- Knowledge is reused across multiple books/projects
- You want maximum separation of concerns

Choose Submodule Split if:
- You need versioned knowledge dependencies
- You want a single checkout but maintain separation
- You're comfortable with git submodule workflow

Choose Monorepo if:
- Privacy is not a concern
- Simplicity is more important than separation
- All content lives in one place

## Principles
- Semantic layer (knowledge) should be protected from accidental modification
- Production layer (pipeline) should read knowledge, not modify it
- Each layer should have independent version history
- Clear boundaries prevent merge conflicts and semantic drift

### Submodule notes
- `git submodule add <repoB> knowledge/blocks`
- **Advantages:** automatically synced folder structure, one checkout.
- **Drawback:** submodules require discipline and care when updating.

### 4. Directory-only split (legacy, weakest)
- Knowledge lives outside the repo entirely (local directory, symlink or mount).
- Pipeline references it via absolute or relative path.
- Works for local experimentation but cannot be shared or versioned cleanly.

## Boundaries
- Never store `blocks/` and `chapters/` in one repository: it mixes meaning and execution.
- Never store candidates in public repo.
- Never allow CI/CD to touch knowledge repo.
- Do not store compiled chapters in the knowledge repo.

## What must live in each repo

### Production repo (book repo)
- `/drafts/chapters/`
- `/pipeline/`
- `/STYLE.md`
- `/README.md`
- build/export scripts

### Knowledge repo
- `/knowledge/INVARIANTS.md`
- `/knowledge/blocks/*.md`
- `/knowledge/candidates/*.md`
- `/knowledge/MAP.md`
- `/knowledge/DECISIONS.md`

## Integration rules
1. Production repo **never writes** to knowledge repo (read-only).
2. Knowledge repo **never contains** output artifacts.
3. Pipeline uses a config entry:
 ```
 knowledge_root: ../book-knowledge-base/knowledge
```
Any change to blocks must be followed by full re-assembly of chapters.

## Confidence

High
