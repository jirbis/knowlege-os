# Backlog — Future Tasks

This file tracks planned features and improvements for the Knowledge Operating System.

---

## ✅ Completed Work

### Agent System Refactor (2024-12-19)
**Status:** Completed  
**Reference:** `implementation_plan_v2.md`

**What was done:**
- ✅ Split agents into separate files (`AGENTS/Extractor.md`, `Organizer.md`, `Assembler.md`, `ArchiveSearch.md`)
- ✅ Rewrote `AGENTS.md` to constitution-only (removed all agent-specific logic)
- ✅ Moved `pipeline.yaml` to `knowledge/pipelines/pipeline.yaml` and updated all references
- ✅ Verified `COMMANDS.md` includes all commands including SEARCH archive
- ✅ Created required directory structure (`AGENTS/`, `knowledge/pipelines/`, `archive/`, `index/`)
- ✅ Updated all documentation for consistency and cross-referencing
- ✅ Added ArchiveSearch support for Telegram exports (documentation)

**Validation:**
- All 4 agent files exist with Command normalization sections
- `AGENTS.md` is constitution-only
- Pipeline path consistency verified (0 non-canonical references)
- All documentation cross-references updated

**Next step:** Final commit pending

---

## 🔌 Connectors & Integrations

### Multi-Repository Architecture Implementation

**Status:** Planned  
**Priority:** Medium  
**Reference:** `knowledge/blocks/frameworks/repository-split-architectures.md`, `knowledge/blocks/frameworks/private-repository-structure.md`, `knowledge/blocks/frameworks/export-chats.md`

Based on the architectural frameworks documented in the knowledge blocks, implement support for multi-repository setups:

#### Task 1: Repository Split Architecture Support ✅
**Status:** Completed  
**Priority:** High

**Description:**
Implement support for dual-repo, submodule, and monorepo split architectures as described in `repository-split-architectures.md`.

**Requirements:**
- ✅ Add configuration support for external knowledge repository paths (`config.yaml`)
- ✅ Implement read-only knowledge repository access patterns
- ✅ Add validation to prevent writing to knowledge repository from pipeline (`tools/validate_repository_boundaries.py`)
- ✅ Support submodule-based integration (`tools/setup_dual_repo.py`)
- ✅ Document integration patterns for each architecture (`docs/Multi-Repository-Setup.md`, `docs/Multi-Repository-Examples.md`)

**Related:**
- Framework: `knowledge/blocks/frameworks/repository-split-architectures.md`
- Should respect boundaries: blocks and chapters never in same repo

**Files Created:**
- `config.yaml` — Main configuration file
- `config.templates/dual-repo.yaml` — Dual-repo template
- `config.templates/submodule.yaml` — Submodule template
- `config.templates/monorepo.yaml` — Monorepo template
- `tools/validate_repository_boundaries.py` — Validation script
- `tools/setup_dual_repo.py` — Dual-repo setup script
- `docs/Multi-Repository-Setup.md` — Complete setup guide
- `docs/Multi-Repository-Examples.md` — Integration examples

#### Task 2: Private Repository Structure Setup ✅
**Status:** Completed  
**Priority:** High

**Description:**
Create tooling and documentation to support the 3-5 repository model described in `private-repository-structure.md`:
- knowledge-os (main system)
- knowledge-base (semantic layer)
- knowledge-chat-archive (raw sources)
- Optional: my-books-N repositories
- Optional: knowledge-shared-templates

**Requirements:**
- ✅ Create repository initialization scripts (`tools/init_repository.py`)
- ✅ Add configuration templates for each repository type (`config.templates/`)
- ✅ Document setup process for multi-repo workflows (`docs/Multi-Repository-Setup.md`)
- ✅ Create validation scripts to enforce repository boundaries (`tools/validate_repository_boundaries.py`)
- ✅ Add integration examples (`docs/Multi-Repository-Examples.md`)

**Related:**
- Framework: `knowledge/blocks/frameworks/private-repository-structure.md`
- Must enforce: production repo never writes to knowledge repo

**Files Created:**
- `tools/init_repository.py` — Repository initialization script
- `tools/README.md` — Tools documentation
- `docs/Multi-Repository-Setup.md` — Complete setup guide
- `docs/Multi-Repository-Examples.md` — Integration examples
- `AGENTS/Assembler.md` — Updated to use config.yaml for knowledge paths

#### Task 3: Chat Archive Repository Integration
**Priority:** High

**Description:**
Implement the chat archive repository pattern from `export-chats.md` with proper separation from main knowledge-os repo.

**Requirements:**
- Create chat archive repository initialization script
- Add configuration for chat archive path (submodule or external)
- Update ArchiveSearch agent to work with external chat archive
- Ensure ArchiveSearch never writes to main knowledge-os repository
- Document chat archive structure and integration

**Related:**
- Framework: `knowledge/blocks/frameworks/export-chats.md`
- Agent: `AGENTS/ArchiveSearch.md`
- Must enforce: raw chats never in `/knowledge/blocks`

---

### Google Docs Connector
**Status:** Planned  
**Priority:** Medium

**Description:**
Create connectors to Google Docs to enable:
- Import content from Google Docs as source material for extraction
- Export assembled content to Google Docs
- Sync knowledge blocks with Google Docs documents

**Requirements:**
- Authentication/authorization with Google API
- Read access to Google Docs (import)
- Write access to Google Docs (export)
- Maintain same non-destructive principles as ArchiveSearch
- Support for document structure preservation

**Related:**
- Similar to ArchiveSearch agent pattern
- Should follow same safety boundaries (read-only for import, controlled write for export)

---

## 📦 Archive & Export Tools

### Telegram Export Tool
**Status:** Planned  
**Priority:** Medium

**Description:**
Create `tools/ingest_telegram_export.py` to support Telegram exports alongside ChatGPT exports.

**Requirements:**
- Parse Telegram export JSON format
- Normalize to same format as ChatGPT exports
- Write to `index/chats.sqlite` with `source="telegram_export"`
- Create normalized markdown in `archive/normalized/`
- Follow same patterns as `ingest_chatgpt_export.py`

**Related:**
- AGENTS/ArchiveSearch.md already updated to support Telegram
- COMMANDS.md already includes Telegram examples
- Documentation updated

---

## 🔍 Search & Discovery

### Multi-source Search Enhancement
**Status:** Planned  
**Priority:** Medium

**Description:**
Enhance search to filter by source type (ChatGPT, Telegram, Google Docs, etc.) and combine results intelligently.

---

## 📝 Notes

- Tasks are listed in rough priority order within each category
- Status: Planned | In Progress | Completed | Blocked
- Priority: High | Medium | Low

---

**Last updated:** 2024-12-19

**Note:** This backlog now includes completed work from `implementation_plan_v2.md` and planned tasks based on architectural frameworks in `knowledge/blocks/frameworks/`.
