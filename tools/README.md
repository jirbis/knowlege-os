# Knowledge OS Tools

Tools for managing Knowledge OS repositories and enforcing boundaries.

---

## Repository Management

### `init_repository.py`

Initialize repository structures for different repository types.

**Usage:**
```bash
python3 tools/init_repository.py <type> [path] [options]
```

**Types:**
- `knowledge-os` — Main system repository
- `knowledge-base` — Semantic layer repository
- `chat-archive` — Chat archive repository
- `book` — Book repository (optional)
- `shared-templates` — Shared templates repository (optional)

**Examples:**
```bash
# Initialize knowledge-os in current directory
python3 tools/init_repository.py knowledge-os .

# Initialize knowledge-base in separate location
python3 tools/init_repository.py knowledge-base ../knowledge-base

# Initialize book repository with name
python3 tools/init_repository.py book ../my-book --book-name "My Book"
```

---

### `setup_dual_repo.py`

Set up dual-repository or submodule architecture.

**Usage:**
```bash
python3 tools/setup_dual_repo.py --knowledge-path <path> [options]
```

**Options:**
- `--knowledge-path` — Path to external knowledge repository (required)
- `--config` — Path to config.yaml (default: ./config.yaml)
- `--submodule` — Set up as git submodule
- `--submodule-url` — Git URL for submodule (required if --submodule)

**Examples:**
```bash
# Set up dual-repo with external path
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# Set up submodule integration
python3 tools/setup_dual_repo.py \
  --knowledge-path ./knowledge \
  --submodule \
  --submodule-url https://github.com/user/knowledge-base.git
```

---

## Validation

### `validate_repository_boundaries.py`

Enforce repository boundaries and validate read-only access patterns.

**Usage:**
```bash
python3 tools/validate_repository_boundaries.py [options]
```

**Options:**
- `--config <path>` — Path to config.yaml (default: ./config.yaml)
- `--check-path <path>` — Check if a specific path is protected
- `--check-knowledge-access` — Check knowledge repository access configuration

**Examples:**
```bash
# Check if a path is protected
python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks

# Check knowledge repository access configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access

# Full validation (both checks)
python3 tools/validate_repository_boundaries.py
```

**Exit codes:**
- `0` — All validations passed
- `1` — Validation failed

**Integration with agents:**
Assembler agent should call this script before write operations:
```bash
python3 tools/validate_repository_boundaries.py --check-path <target-path>
```

---

## Archive & Search

### `ingest_chatgpt_export.py`

Ingest ChatGPT export into FTS5 index.

### `ingest_telegram_export.py`

(To be created) Ingest Telegram export into FTS5 index.

### `search_archive.py`

Search indexed conversations.

### `extract_snippet.py`

Extract conversation snippet by ID.

---

## Related Documentation

- **Multi-Repository Setup:** `docs/Multi-Repository-Setup.md`
- **Configuration:** `config.yaml`, `config.templates/`
- **Architectures:** `knowledge/blocks/frameworks/repository-split-architectures.md`
