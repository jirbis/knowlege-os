---
type: framework
themes:
  - repository-architecture
  - knowledge-management
  - archive-management
confidence: high
reuse:
  - blog
  - book
  - consulting
source: chat
tags:
  - repository
  - architecture
  - chatgpt
  - archive
  - knowledge-os
---

# Where to Store Raw ChatGPT Conversation Sources

## Claim
Raw ChatGPT conversations must be stored outside the main knowledge-os repository to avoid mixing semantic decisions with unprocessed chat data, prevent repository pollution, and enable safe long-term reference, search, and extraction.

## Why it matters
Chats are **not knowledge** — they are noisy, inconsistent, and often contradictory.  
If raw chats enter the main repository:
- Knowledge-os structure breaks down
- Git history gets polluted with gigabytes of raw text
- Extractor starts working "on top of garbage"
- Risk of accidentally committing private data increases
- Semantic drift begins

Separating chat-raw-archive makes the system stable: raw material → processing → blocks.

## Recommended Storage Location
A **separate private repository** dedicated to raw chat archives.

```
knowledge-chat-archive/
  threads/
  raw/
  metadata.json
  index.sqlite (optional FTS)
```

This repository can be:
- a **private GitHub repo**, or
- a **local-only git repo**, or
- a **submodule** inside knowledge-os (read-only).

## Integration Path
Inside knowledge-os:

```
knowledge-os/
  knowledge/
  agents/
  pipeline/
  chat_archive/  # submodule or external directory
```

Configuration example:

```yaml
paths:
  knowledge_root: ./knowledge
  chat_archive: ../knowledge-chat-archive/
```

## Boundaries
- Raw chats must not live in `/knowledge/blocks`.
- Raw chats must not be committed to the main repository.
- Extractor and ArchiveSearch may read from the archive, but must never write to it.
- Only curated blocks/invariants enter the knowledge layer; chats serve solely as evidence.

## Evidence (from prior analysis)
- Mixing raw chats with semantic blocks broke earlier agent systems.
- Raw GPT output often contains contradictions; storing it next to blocks risks semantic drift.
- Dedicated archives allow FTS indexing, citations, and traceability without contaminating meaning-layer.

## Used in
- Repository split design.
- Knowledge ingestion guidelines.
- ArchiveSearch agent specification.

## Confidence

High
