---
type: framework
themes:
  - repository-architecture
  - knowledge-management
  - system-design
confidence: high
reuse:
  - blog
  - book
  - consulting
source: chat
tags:
  - repository
  - architecture
  - knowledge-os
  - multi-repo
---

# Required Repositories for the Knowledge-OS System

## Claim
A complete AI-assisted book-writing system requires at least three separate repositories: (1) the production/pipeline repository, (2) the semantic knowledge repository, and (3) the raw chat archive repository.

## Why it matters
Keeping execution logic, semantic knowledge, and raw conversational sources in a single Git repository leads to broken architecture: polluted history, privacy leaks, semantic drift, and coupling between thinking and output. A split-repository model enforces separation of concerns and enables safe evolution of each layer.

## Repository Naming (Configurable)

**Important:** The repository names shown below are **default examples** and can be customized to match your naming conventions, project structure, or organizational requirements.

The framework focuses on **roles and responsibilities**, not specific names. You can use any names that make sense for your context, as long as the separation of concerns is maintained.

**Default names (examples):**
- `knowledge-os` → Main system repository (customizable)
- `knowledge-base` → Semantic layer repository (customizable)
- `knowledge-chat-archive` → Chat archive repository (customizable)
- `my-books-N` → Book repository pattern (customizable)
- `knowledge-shared-templates` → Templates repository (customizable)

**Customization:**
- Configure repository names in `config.yaml` via `knowledge.root_path` and `chat_archive.root_path`
- Repository initialization tools (`tools/init_repository.py`) accept custom paths
- Only the **structural roles** (main system, semantic layer, archive) are fixed; names are flexible

---

## Repository 1 — **Main System Repository** (default: `knowledge-os`)

**Purpose:** execution + orchestration  
**Customizable name:** Yes (default: `knowledge-os`, `pipeline-repo`, `main-system`, etc.)  
Contains everything needed to *assemble* chapters from blocks.

**Default structure (example):**
```
knowledge-os/          # ← Customizable name
  agents/
  pipeline/
  drafts/
  output/
  STYLE.md
  README.md
```

**Responsibilities:**
- Stores AGENTS (Extractor, Organizer, Assembler, Critic)
- Stores pipeline logic (phases, gates, assembly rules)
- Assembles chapters (chXX.md) from blocks
- Does NOT contain raw chats
- Does NOT contain blocks

**Configuration:**
- Path configured in `config.yaml` (if using external knowledge repository)
- Repository name can be any identifier matching your naming convention

---

## Repository 2 — **Semantic Layer Repository** (default: `knowledge-base`)

**Purpose:** source of truth for meaning  
**Customizable name:** Yes (default: `knowledge-base`, `semantic-repo`, `blocks-repo`, etc.)  
This is the **semantic repository** — the heart of your system.

**Default structure (example):**
```
knowledge-base/        # ← Customizable name
  knowledge/
    INVARIANTS.md
    DECISIONS.md
    MAP.md
    blocks/
    candidates/
```

**Responsibilities:**
- Stores assertions, not texts
- Records decisions (semantic commits)
- Manages blocks and boundaries
- Forbidden for editing by agents except Extractor/Organizer
- Can be private

**Integration:**
- Used by main system repository as read-only
- Path configured in `config.yaml` via `knowledge.root_path`
- Default example path: `../knowledge-base/knowledge` (customizable)

---

## Repository 3 — **Chat Archive Repository** (default: `knowledge-chat-archive`)

**Purpose:** storage of ChatGPT/Telegram conversation sources  
**Customizable name:** Yes (default: `knowledge-chat-archive`, `chat-archive`, `conversations-repo`, etc.)  
Raw chats = raw evidence field → *never* enter pipeline or blocks.

**Default structure (example):**
```
knowledge-chat-archive/  # ← Customizable name
  threads/
    thread-001/
      000-system.md
      010-user.md
      020-assistant.md
      metadata.json
  raw/
  index.sqlite (optional FTS5)
  README.md
```

**Responsibilities:**
- Stores chat sources (as evidence)
- FTS search for ArchiveSearch agents
- Private repository (required)
- Read-only for main system repository

**Integration:**
- Synced via submodule or explicit path
- Path configured in `config.yaml` via `chat_archive.root_path`
- Default example path: `../knowledge-chat-archive` (customizable)

---

## Optional Repository 4 — **Book Repository** (default pattern: `my-books-N`)

**Purpose:** final manuscript + publishing pipeline  
**Customizable name:** Yes (default pattern: `my-books-N`, `book-<title>`, `<project>-book`, etc.)  
If you write multiple books, each book is a separate repository.

**Default structure (example):**
```
book-ai-orchestration/  # ← Customizable name pattern
  chapters/
  outline/
  cover/
  publishing/
  README.md
```

**Responsibilities:**
- Stores final deliverable texts
- Stores book materials
- Imports blocks read-only
- Does not contain raw chats
- Clean, lightweight, public (if needed)

**Naming examples:**
- `my-books-1`, `my-books-2` (default pattern)
- `book-ai-orchestration`, `book-knowledge-systems`
- `ai-book`, `knowledge-book`
- Any name matching your project structure

---

## Optional Repository 5 — **Templates Repository** (default: `knowledge-shared-templates`)

**Purpose:** tools shared across books/projects  
**Customizable name:** Yes (default: `knowledge-shared-templates`, `shared-templates`, `templates-repo`, etc.)

**Default structure (example):**
```
knowledge-shared-templates/  # ← Customizable name
  block-template.md
  chapter-template.md
  pipeline-templates/
  agents-templates/
```

**Responsibilities:**
- Unified set of templates for all books
- Facilitates updates

**Naming examples:**
- `knowledge-shared-templates` (default)
- `shared-templates`, `templates-repo`
- `my-templates`, `common-templates`
- Any name matching your organization

---

## Summary Table

| Repo (Default Name) | Customizable | Role | Contains | Must Not Contain |
|---------------------|--------------|------|----------|------------------|
| **knowledge-os** (main system) | ✅ Yes | execution & orchestration | agents, pipeline, drafts | blocks, raw chats |
| **knowledge-base** (semantic layer) | ✅ Yes | semantic meaning | blocks, invariants, decisions | pipeline, chapters |
| **knowledge-chat-archive** (archive) | ✅ Yes | raw sources | ChatGPT/Telegram conversations | draft blocks, chapters |
| **my-books-N** (book repos, optional) | ✅ Yes | final book | chapters, cover | blocks, chats |
| **knowledge-shared-templates** (templates, optional) | ✅ Yes | templates | block/chapter/pipeline templates | ∅ |

**Note:** All repository names are configurable. The table shows default examples. The important aspect is maintaining the **role separation**, not the specific names.

## Customization Guidelines

### Configuring Custom Repository Names

1. **Main System Repository:**
   - Use any name (e.g., `pipeline-repo`, `main-system`, `kos-core`)
   - No configuration needed (this is the root repository)

2. **Knowledge Repository:**
   - Set path in `config.yaml`: `knowledge.root_path: "../your-custom-name/knowledge"`
   - Or: `knowledge.root_path: "/absolute/path/to/your-custom-repo/knowledge"`

3. **Chat Archive Repository:**
   - Set path in `config.yaml`: `chat_archive.root_path: "../your-custom-archive-name"`
   - Or: `chat_archive.root_path: "/absolute/path/to/your-archive"`

4. **Book Repositories:**
   - Initialize with custom name: `python3 tools/init_repository.py book ../your-book-name --book-name "Your Book"`
   - Use any naming pattern that suits your workflow

5. **Templates Repository:**
   - Initialize with custom path: `python3 tools/init_repository.py shared-templates ../your-templates-name`
   - Use any name matching your organization

### Important Principles

- **Role separation** is mandatory (e.g., blocks and pipeline must be separate)
- **Repository names** are flexible (choose names that match your conventions)
- **Paths** are configured in `config.yaml` (supports relative and absolute paths)
- **Validation** enforces boundaries regardless of repository names

---

## Confidence

High