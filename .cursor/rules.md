# .cursor/rules.md
# Minimal Rules for Cursor in the Knowledge-OS System

Cursor works inside Knowledge OS, which supports multiple repository architectures:

- **Monorepo** — Single repository with strict boundaries (default)
- **Dual-Repo** — Separate repositories (knowledge and pipeline)
- **Submodule** — Git submodule integration

Repository names are **configurable**. The framework focuses on **roles and responsibilities**, not specific names.

**Repository roles:**
1. **Main System Repository** (default: `knowledge-os`) — execution & assembly (this repo)
2. **Semantic Layer Repository** (default: `knowledge-base`) — semantic layer (blocks, invariants)
3. **Chat Archive Repository** (default: `knowledge-chat-archive`) — raw chats (read-only)

**Configuration:** Repository paths are configured in `config.yaml`. Read `knowledge.root_path` and `chat_archive.root_path` to determine actual paths.

Cursor must follow the rules below.

---

## 1. Allowed Write Locations

Cursor may write ONLY to paths relative to the current repository root:

**In monorepo (default):**
- `./drafts/`
- `./output/`
- `./knowledge/blocks/` (if internal)
- `./knowledge/candidates/` (if internal)
- `./knowledge/MAP.md` (if internal)
- `./knowledge/DECISIONS.md` (if internal)

**In dual-repo or submodule architecture:**
- Read paths from `config.yaml`:
  - Main repo: `./drafts/`, `./output/` (always allowed)
  - Knowledge repo: Use `config.yaml` → `knowledge.root_path` to determine path
  - Knowledge repo paths (read-only from main repo):
    - `{knowledge.root_path}/blocks/`
    - `{knowledge.root_path}/candidates/`
    - `{knowledge.root_path}/MAP.md`
    - `{knowledge.root_path}/DECISIONS.md`

**Validation:** Always run `python3 tools/validate_repository_boundaries.py --check-path <path>` before writing.

Everything else is **read-only**.

---

## 2. Agent Role Boundaries

### Extractor
- Extracts blocks/candidates from chats or drafts.
- Writes only to knowledge repository (path from `config.yaml` → `knowledge.root_path`).
- Commands: `EXTRACT conclusion|framework|checklist|narrative|metaphor`
- No invention.

### Organizer
- Merges/splits/refines blocks.
- Commands: `ORGANIZE knowledge blocks|themes|duplicates`
- No meaning change.
- Proposes changes, never applies automatically.

### Assembler
- Builds content from blocks + candidates.
- Commands: `ASSEMBLE blog|article|book|email`
- Reads knowledge repository path from `config.yaml`.
- Writes only to `./output/` (or path from `config.yaml` → `pipeline.output_dir`).
- Validates paths using `tools/validate_repository_boundaries.py`.
- No new claims, no creativity.

### ArchiveSearch
- Searches chat archive (ChatGPT/Telegram exports).
- Command: `SEARCH archive export_path=<path> query="<fts query>"`
- Reads archive path from `config.yaml` → `chat_archive.root_path`.
- Read-only.
- Never writes to knowledge repository.

---

## 3. Canonical Commands Only

**Source of truth:** `COMMANDS.md` — Only commands defined there are valid.

### Allowed Commands (from COMMANDS.md):

**EXTRACT:**
- `EXTRACT conclusion`
- `EXTRACT framework`
- `EXTRACT checklist`
- `EXTRACT narrative`
- `EXTRACT metaphor`

**MARK:**
- `MARK as book_chapter candidate`
- `MARK as book_section candidate`
- `MARK as article candidate`
- `MARK as blog_post candidate`

**ORGANIZE:**
- `ORGANIZE knowledge blocks`
- `ORGANIZE themes`
- `ORGANIZE duplicates`

**ASSEMBLE:**
- `ASSEMBLE blog`
- `ASSEMBLE article`
- `ASSEMBLE book`
- `ASSEMBLE email`

**SUGGEST (advisory only, never writes):**
- `SUGGEST extract`
- `SUGGEST organization`
- `SUGGEST assembly`

**SET:**
- `SET status: draft`
- `SET status: solid`
- `SET status: used`
- `SET status: deprecated`

**SEARCH (read-only):**
- `SEARCH archive export_path=<path> query="<fts query>" [source_type=<chatgpt|telegram>] [limit=<int>]`

### Reject everything else.
Response:
> Use canonical commands only. See COMMANDS.md for valid commands.

---

## 4. Meaning Safety Rules

- **No invention**: agents cannot create new claims.
- **No drift**: assembled content must match blocks exactly.
- **No style rewriting**: follow `STYLE.md` if present.
- **One source of truth**:  
  invariants → blocks → candidates → output.
- **No cross-contamination**:  
  blocks never go into pipeline repo (enforced by validation);  
  chats never go into knowledge repository.
- **Repository boundaries**: Always validate paths using `tools/validate_repository_boundaries.py`.

---

## 5. Stop Conditions (must refuse)

Cursor must stop when:
- asked to write outside allowed dirs  
- asked to generate new ideas/examples/claims  
- asked to modify invariants  
- MAP references missing blocks  
- candidates leak into chapters  
- user requests “creativity” for Assembler/Extractor  

Response:
> Stopping: this action violates Knowledge-OS rules.

---

## 6. Simple Workflow

1. `SEARCH archive export_path=<path> query="<fts query>"` — Find relevant conversations
2. `EXTRACT conclusion|framework|checklist|...` — Extract valuable insights
3. `MARK as book_chapter candidate|article candidate|...` — Mark potential content
4. `ORGANIZE knowledge blocks` — Maintain coherence (optional, periodic)
5. `ASSEMBLE blog|article|book|email` — Build content from blocks
6. Review output — Ensure no drift from source blocks

---

## 7. Definition of Done

- No drift from source blocks
- No new claims (only from existing blocks)
- No unresolved candidates (if using candidates workflow)
- All assemblies use valid source references
- Output paths validated (using `tools/validate_repository_boundaries.py`)
- Repository boundaries respected (from `config.yaml`)
- Output reproducible (from blocks)

## 8. Repository Configuration

Always check `config.yaml` to determine:
- Knowledge repository path: `knowledge.root_path`
- Chat archive path: `chat_archive.root_path`
- Architecture type: `architecture` (monorepo|dual-repo|submodule)
- Protected paths: `boundaries.protected_paths`
- Allowed output paths: `boundaries.allowed_output_paths`

**Example (monorepo):**
```yaml
architecture: "monorepo"
knowledge:
  root_path: "./knowledge"  # Internal
```

**Example (dual-repo):**
```yaml
architecture: "dual-repo"
knowledge:
  root_path: "../knowledge-base/knowledge"  # External, customizable name
  read_only: true
```

Paths are resolved relative to the main system repository root.  
