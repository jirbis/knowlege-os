# Multi-Repository Setup Guide

Complete guide for setting up Knowledge OS with multi-repository architectures.

---

## Overview

Knowledge OS supports three repository architectures:

1. **Dual-Repo Split** (recommended) — Two separate repositories
2. **Submodule Split** — Git submodule integration
3. **Monorepo** — Single repository with strict boundaries

**Important:** Repository names shown in examples (e.g., `knowledge-os`, `knowledge-base`) are **default examples** and are fully configurable. You can use any repository names that match your naming conventions, as long as the role separation is maintained.

For detailed architecture information, see:
- `knowledge/blocks/frameworks/repository-split-architectures.md`
- `knowledge/blocks/frameworks/private-repository-structure.md` — Includes customization guidelines

---

## Quick Start

### Option 1: Initialize from Scratch

**Note:** Repository names in examples (`knowledge-os`, `knowledge-base`) are defaults and can be customized.

```bash
# Initialize main system repository (default name: knowledge-os)
python3 tools/init_repository.py knowledge-os /path/to/your-main-repo

# Initialize knowledge repository (default name: knowledge-base, customizable)
python3 tools/init_repository.py knowledge-base /path/to/your-knowledge-repo

# Initialize chat archive repository (default name: knowledge-chat-archive, customizable)
python3 tools/init_repository.py chat-archive /path/to/your-archive-repo

# Set up dual-repo configuration (use your custom path)
python3 tools/setup_dual_repo.py --knowledge-path ../your-knowledge-repo/knowledge
```

**Customization:** Use any paths and names that match your conventions. Configure paths in `config.yaml`.

### Option 2: Use Configuration Templates

Copy the appropriate template to `config.yaml`:

```bash
# For dual-repo
cp config.templates/dual-repo.yaml config.yaml

# For submodule
cp config.templates/submodule.yaml config.yaml

# For monorepo
cp config.templates/monorepo.yaml config.yaml
```

Then edit `config.yaml` to match your paths.

---

## Architecture 1: Dual-Repo Split (Recommended)

**Best for:** Privacy, composability, multi-book knowledge reuse

### Setup Steps

1. **Create repositories separately:**
   ```bash
   # Create knowledge-os (main system)
   mkdir knowledge-os && cd knowledge-os
   git init
   python3 tools/init_repository.py knowledge-os .
   
   # Create knowledge-base (semantic layer) in different location
   cd ..
   mkdir knowledge-base && cd knowledge-base
   git init
   python3 tools/init_repository.py knowledge-base .
   ```

2. **Configure knowledge-os to use external knowledge-base:**
   ```bash
   cd knowledge-os
   python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge
   ```

3. **Verify configuration:**
   ```bash
   python3 tools/validate_repository_boundaries.py --check-knowledge-access
   ```

### Directory Structure

**Note:** Repository names shown are default examples and can be customized.

```
/parent-directory/
  knowledge-os/           # Main system (default name, customizable)
    AGENTS/
    pipeline/
    drafts/
    output/
    config.yaml          # Points to ../knowledge-base/knowledge (or your custom path)
  
  knowledge-base/        # Semantic layer (default name, customizable)
    knowledge/
      blocks/
      candidates/
      INVARIANTS.md
      DECISIONS.md
      MAP.md
```

**Customization:** Repository names can be changed (e.g., `pipeline-repo`, `semantic-repo`). Update paths in `config.yaml` accordingly.

### Configuration (`config.yaml`)

```yaml
architecture: "dual-repo"

knowledge:
  root_path: "../knowledge-base/knowledge"
  integration: "external"
  read_only: true
  enforce_read_only: true
```

---

## Architecture 2: Submodule Split

**Best for:** Versioned knowledge dependencies, single checkout workflow

### Setup Steps

1. **Create knowledge-base repository first:**
   ```bash
   mkdir knowledge-base && cd knowledge-base
   git init
   python3 tools/init_repository.py knowledge-base .
   git add .
   git commit -m "Initial knowledge-base repository"
   # Push to remote if needed
   ```

2. **Create knowledge-os and add submodule:**
   ```bash
   mkdir knowledge-os && cd knowledge-os
   git init
   python3 tools/init_repository.py knowledge-os .
   
   # Add knowledge-base as submodule
   python3 tools/setup_dual_repo.py \
     --knowledge-path ./knowledge \
     --submodule \
     --submodule-url <git-url-to-knowledge-base>
   ```

3. **Verify configuration:**
   ```bash
   python3 tools/validate_repository_boundaries.py --check-knowledge-access
   ```

### Directory Structure

```
knowledge-os/           # Main repository
  AGENTS/
  pipeline/
  output/
  knowledge/           # Git submodule → knowledge-base
    blocks/
    candidates/
    ...
  .gitmodules          # Git submodule configuration
  config.yaml          # Points to ./knowledge
```

### Configuration (`config.yaml`)

```yaml
architecture: "submodule"

knowledge:
  root_path: "./knowledge"
  integration: "submodule"
  submodule_path: "./knowledge"
  read_only: true
  enforce_read_only: true
```

---

## Architecture 3: Monorepo

**Best for:** Simplicity, single source of truth, when privacy is not a concern

### Setup Steps

1. **Initialize as monorepo:**
   ```bash
   mkdir knowledge-os && cd knowledge-os
   git init
   python3 tools/init_repository.py knowledge-os .
   ```

2. **Use monorepo template:**
   ```bash
   cp config.templates/monorepo.yaml config.yaml
   ```

3. **Verify boundaries are enforced:**
   ```bash
   python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks
   # Should show: OK (protected paths are validated)
   ```

### Directory Structure

```
knowledge-os/           # Single repository
  AGENTS/
  knowledge/           # Internal, but protected
    blocks/
    candidates/
    pipelines/
  pipeline/
  output/
  config.yaml
```

### Configuration (`config.yaml`)

```yaml
architecture: "monorepo"

knowledge:
  root_path: "./knowledge"
  integration: "internal"
  read_only: false
  enforce_read_only: true  # Still enforce via validation
```

---

## Repository Types Reference

**Important:** Repository names shown below are **default examples** and can be customized. See [Customizing Repository Names](#customizing-repository-names) section below.

### 1. Main System Repository (default: `knowledge-os`)

**Purpose:** Execution and orchestration  
**Customizable name:** ✅ Yes (default: `knowledge-os`, `pipeline-repo`, `main-system`, etc.)

**Contains:**
- `AGENTS/` — Agent specifications
- `pipeline/` — Assembly pipeline logic
- `drafts/` — Draft chapters
- `output/` — Generated content
- `config.yaml` — Configuration

**Must NOT contain:**
- Knowledge blocks
- Raw chats

**Initialize:**
```bash
# Default name
python3 tools/init_repository.py knowledge-os /path/to/knowledge-os

# Custom name (use any path/name you prefer)
python3 tools/init_repository.py knowledge-os /path/to/your-custom-name
```

### 2. Semantic Layer Repository (default: `knowledge-base`)

**Purpose:** Source of truth for meaning  
**Customizable name:** ✅ Yes (default: `knowledge-base`, `semantic-repo`, `blocks-repo`, etc.)

**Contains:**
- `knowledge/blocks/` — Atomic knowledge blocks
- `knowledge/candidates/` — Content candidates
- `knowledge/INVARIANTS.md` — Invariants
- `knowledge/DECISIONS.md` — Decisions log
- `knowledge/MAP.md` — Knowledge map

**Must NOT contain:**
- Pipeline logic
- Output chapters
- Raw chats

**Initialize:**
```bash
# Default name
python3 tools/init_repository.py knowledge-base /path/to/knowledge-base

# Custom name
python3 tools/init_repository.py knowledge-base /path/to/your-semantic-repo
```

**Configuration:** Set path in `config.yaml`:
```yaml
knowledge:
  root_path: "../your-custom-name/knowledge"  # Use your custom path
```

### 3. Chat Archive Repository (default: `knowledge-chat-archive`)

**Purpose:** Storage of ChatGPT/Telegram conversations  
**Customizable name:** ✅ Yes (default: `knowledge-chat-archive`, `chat-archive`, `conversations-repo`, etc.)

**Contains:**
- `threads/` — Conversation threads
- `raw/` — Raw exports
- `index/` — FTS5 index (optional)

**Must NOT contain:**
- Knowledge blocks
- Pipeline logic
- Output chapters

**Initialize:**
```bash
# Default name
python3 tools/init_repository.py chat-archive /path/to/knowledge-chat-archive

# Custom name
python3 tools/init_repository.py chat-archive /path/to/your-archive-repo
```

**Configuration:** Set path in `config.yaml`:
```yaml
chat_archive:
  root_path: "../your-custom-archive-name"  # Use your custom path
```

### 4. Book Repository (default pattern: `my-books-N`)

**Purpose:** Final manuscript and publishing  
**Customizable name:** ✅ Yes (default pattern: `my-books-N`, `book-<title>`, `<project>-book`, etc.)

**Contains:**
- `chapters/` — Final chapters
- `outline/` — Book outline
- `cover/` — Cover materials
- `publishing/` — Publishing assets

**Must NOT contain:**
- Knowledge blocks
- Raw chats

**Initialize:**
```bash
# Default pattern
python3 tools/init_repository.py book /path/to/my-books-1 --book-name "My First Book"

# Custom name
python3 tools/init_repository.py book /path/to/ai-orchestration-book --book-name "AI Orchestration"
```

### 5. Templates Repository (default: `knowledge-shared-templates`)

**Purpose:** Templates shared across projects  
**Customizable name:** ✅ Yes (default: `knowledge-shared-templates`, `shared-templates`, `templates-repo`, etc.)

**Contains:**
- `block-templates/`
- `chapter-templates/`
- `pipeline-templates/`
- `agents-templates/`

**Initialize:**
```bash
# Default name
python3 tools/init_repository.py shared-templates /path/to/knowledge-shared-templates

# Custom name
python3 tools/init_repository.py shared-templates /path/to/your-templates-repo
```

---

## Customizing Repository Names

All repository names in the framework are **configurable** and can be customized to match your naming conventions, organizational structure, or project requirements.

### Principles

- **Role separation** is mandatory (e.g., blocks and pipeline must be separate)
- **Repository names** are flexible (choose names that match your conventions)
- **Paths** are configured in `config.yaml` (supports relative and absolute paths)
- **Validation** enforces boundaries regardless of repository names

### How to Customize

1. **Choose your repository names** based on your naming conventions
2. **Initialize repositories** with your chosen paths/names
3. **Configure paths** in `config.yaml` to point to your custom repository locations
4. **Update tools** if needed (all tools accept custom paths)

### Examples

**Default names:**
- `knowledge-os`, `knowledge-base`, `knowledge-chat-archive`

**Custom naming examples:**
- `pipeline-repo`, `semantic-repo`, `chat-archive` (simpler)
- `kos-core`, `kos-knowledge`, `kos-archive` (prefixed)
- `main-system`, `blocks-repo`, `conversations-repo` (descriptive)
- `my-pipeline`, `my-knowledge`, `my-archive` (personal)
- Any names matching your organization's conventions

### Configuration Example

```yaml
# config.yaml with custom repository names
knowledge:
  root_path: "../semantic-repo/knowledge"  # Custom name: semantic-repo
  integration: "external"
  read_only: true

chat_archive:
  root_path: "../conversations-repo"  # Custom name: conversations-repo
  integration: "external"
  read_only: true
```

For complete customization guidelines, see `knowledge/blocks/frameworks/private-repository-structure.md`.

---

## Validation

### Validate Repository Boundaries

```bash
# Check if a path is protected
python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks

# Check knowledge repository access configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access

# Check everything
python3 tools/validate_repository_boundaries.py
```

### Validate Before Operations

The validation script should be run:
- Before assembly operations (ASSEMBLE command)
- During CI/CD pipelines
- When setting up new repository structures

---

## Integration Rules

### Rule 1: Production Repo Never Writes to Knowledge Repo

The knowledge repository is **read-only** from the production repository's perspective.

**Enforcement:**
- Configuration: `knowledge.enforce_read_only: true`
- Validation script: `tools/validate_repository_boundaries.py`
- Assembler agent must validate paths before writing

### Rule 2: Knowledge Repo Never Contains Output Artifacts

The knowledge repository must not contain:
- Compiled chapters
- Draft content
- Output files
- Pipeline scripts

### Rule 3: Pipeline Uses Config Entry

Pipeline reads knowledge blocks from the path specified in `config.yaml`:

```yaml
knowledge:
  root_path: "../knowledge-base/knowledge"
```

Any change to blocks requires full re-assembly of chapters.

---

## Common Workflows

### Workflow: Setting Up Dual-Repo from Scratch

```bash
# 1. Initialize repositories
python3 tools/init_repository.py knowledge-os ./knowledge-os
python3 tools/init_repository.py knowledge-base ./knowledge-base

# 2. Configure dual-repo
cd knowledge-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 3. Verify
python3 tools/validate_repository_boundaries.py

# 4. Test
python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks
# Should fail (protected path)
```

### Workflow: Adding Submodule

```bash
# 1. Ensure knowledge-base is a git repository
cd knowledge-base
git init
git add .
git commit -m "Initial commit"
# Push to remote

# 2. In knowledge-os, add as submodule
cd ../knowledge-os
python3 tools/setup_dual_repo.py \
  --knowledge-path ./knowledge \
  --submodule \
  --submodule-url <git-url>

# 3. Verify
python3 tools/validate_repository_boundaries.py --check-knowledge-access
```

### Workflow: Migrating from Monorepo to Dual-Repo

```bash
# 1. Extract knowledge/ directory to separate repo
cd knowledge-os
git subtree push --prefix=knowledge origin knowledge-base

# Or manually:
mkdir ../knowledge-base
cp -r knowledge/* ../knowledge-base/
cd ../knowledge-base
git init
git add .
git commit -m "Extracted knowledge-base"

# 2. Configure dual-repo
cd ../knowledge-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 3. Remove knowledge/ from knowledge-os (keep structure if needed)
# Update .gitignore if needed
```

---

## Troubleshooting

### Issue: "Write operation forbidden"

**Solution:** Check that you're not trying to write to protected paths:
```bash
python3 tools/validate_repository_boundaries.py --check-path <your-path>
```

### Issue: "Knowledge repository access validation failed"

**Solution:** Check `config.yaml`:
- External repos must have `read_only: true`
- `enforce_read_only: true` must be set

### Issue: Submodule not found

**Solution:**
```bash
# Initialize submodules
git submodule update --init --recursive

# Or clone with submodules
git clone --recursive <repo-url>
```

---

## Related Documentation

- **Architectures:** `knowledge/blocks/frameworks/repository-split-architectures.md`
- **Repository Structure:** `knowledge/blocks/frameworks/private-repository-structure.md`
- **Chat Archive:** `knowledge/blocks/frameworks/export-chats.md`
- **Agent Specifications:** `AGENTS/Assembler.md` (for pipeline integration)

---

## Configuration Reference

See `config.yaml` for full configuration options and `config.templates/` for architecture-specific templates.
