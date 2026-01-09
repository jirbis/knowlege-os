# Multi-Repository Integration Examples

Practical examples of integrating Knowledge OS with multi-repository setups.

---

## Example 1: Dual-Repo Setup from Scratch

### Scenario
Setting up a new Knowledge OS system with separate repositories for privacy and reuse across multiple projects.

### Steps

```bash
# 1. Create and initialize knowledge-os
mkdir knowledge-os && cd knowledge-os
git init
python3 tools/init_repository.py knowledge-os .

# 2. Create and initialize knowledge-base (separate location)
cd ..
mkdir knowledge-base && cd knowledge-base
git init
python3 tools/init_repository.py knowledge-base .
git add .
git commit -m "Initial knowledge-base repository"

# 3. Configure knowledge-os to use external knowledge-base
cd ../knowledge-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 4. Verify configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access

# 5. Test validation
python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks
# Expected: ERROR (path is protected)

python3 tools/validate_repository_boundaries.py --check-path ./output/blog
# Expected: OK (path is allowed)
```

### Result

```
knowledge-os/
  config.yaml              # Points to ../knowledge-base/knowledge
  AGENTS/
  pipeline/
  output/
  ...

../knowledge-base/
  knowledge/
    blocks/
    candidates/
    INVARIANTS.md
    ...
```

### Configuration (`knowledge-os/config.yaml`)

```yaml
architecture: "dual-repo"

knowledge:
  root_path: "../knowledge-base/knowledge"
  integration: "external"
  read_only: true
  enforce_read_only: true
```

---

## Example 2: Submodule Integration

### Scenario
Setting up Knowledge OS with git submodule for versioned knowledge dependencies and single checkout.

### Steps

```bash
# 1. Create knowledge-base repository first (with remote)
mkdir knowledge-base && cd knowledge-base
git init
python3 tools/init_repository.py knowledge-base .
git add .
git commit -m "Initial knowledge-base"
git remote add origin https://github.com/user/knowledge-base.git
git push -u origin main

# 2. Create knowledge-os repository
cd ..
mkdir knowledge-os && cd knowledge-os
git init
python3 tools/init_repository.py knowledge-os .

# 3. Add knowledge-base as submodule
python3 tools/setup_dual_repo.py \
  --knowledge-path ./knowledge \
  --submodule \
  --submodule-url https://github.com/user/knowledge-base.git

# 4. Initialize submodule (if needed)
git submodule update --init --recursive

# 5. Verify
python3 tools/validate_repository_boundaries.py --check-knowledge-access
```

### Result

```
knowledge-os/
  .gitmodules              # Git submodule configuration
  knowledge/              # Submodule → knowledge-base
    blocks/
    candidates/
    ...
  config.yaml             # Points to ./knowledge
  ...
```

### Configuration (`knowledge-os/config.yaml`)

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

## Example 3: Monorepo with Strict Boundaries

### Scenario
Single repository setup with enforced separation between knowledge and pipeline layers.

### Steps

```bash
# 1. Initialize monorepo
mkdir knowledge-os && cd knowledge-os
git init
python3 tools/init_repository.py knowledge-os .

# 2. Use monorepo template
cp config.templates/monorepo.yaml config.yaml

# 3. Verify boundaries are enforced
python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks
# Should show protected

python3 tools/validate_repository_boundaries.py --check-path ./output/blog
# Should show allowed
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

## Example 4: Complete Multi-Repo System (5 Repositories)

### Scenario
Full setup with all repository types: knowledge-os, knowledge-base, chat-archive, book, and shared-templates.

### Steps

```bash
# 1. Initialize all repositories
python3 tools/init_repository.py knowledge-os ./knowledge-os
python3 tools/init_repository.py knowledge-base ./knowledge-base
python3 tools/init_repository.py chat-archive ./knowledge-chat-archive
python3 tools/init_repository.py book ./my-book-1 --book-name "My First Book"
python3 tools/init_repository.py shared-templates ./knowledge-shared-templates

# 2. Configure knowledge-os
cd knowledge-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 3. Manually update config.yaml for chat archive
# Edit config.yaml:
# chat_archive:
#   root_path: "../knowledge-chat-archive"
#   integration: "external"
#   read_only: true

# 4. Verify all boundaries
python3 tools/validate_repository_boundaries.py
```

### Directory Structure

```
workspace/
  knowledge-os/              # Main system
    config.yaml              # References external repos
    AGENTS/
    pipeline/
    output/
  
  knowledge-base/            # Semantic layer
    knowledge/
      blocks/
      candidates/
      INVARIANTS.md
      DECISIONS.md
      MAP.md
  
  knowledge-chat-archive/    # Raw sources
    threads/
    raw/
    index/
  
  my-book-1/                 # Book repository
    chapters/
    outline/
    cover/
    publishing/
  
  knowledge-shared-templates/ # Shared templates
    block-templates/
    chapter-templates/
    ...
```

---

## Example 5: Migration from Monorepo to Dual-Repo

### Scenario
Migrating existing monorepo to dual-repo architecture.

### Steps

```bash
# 1. Backup current repository
cp -r knowledge-os knowledge-os-backup
cd knowledge-os

# 2. Extract knowledge/ to separate repository
cd ..
mkdir knowledge-base && cd knowledge-base
git init
# Copy knowledge directory content
cp -r ../knowledge-os/knowledge/* .
git add .
git commit -m "Extracted knowledge-base from monorepo"
# Push to remote if needed

# 3. Configure knowledge-os for dual-repo
cd ../knowledge-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 4. Remove knowledge/ from knowledge-os (optional, can keep as reference)
# Or update .gitignore if keeping structure

# 5. Verify boundaries
python3 tools/validate_repository_boundaries.py
```

---

## Example 6: Assembler Integration with External Knowledge Repo

### Scenario
Using Assembler agent with external knowledge repository.

### Workflow

1. **Configuration check:**
   ```bash
   # Verify config.yaml has correct path
   cat config.yaml | grep knowledge -A 5
   ```

2. **Before assembly, validate:**
   ```bash
   # Assembler should run this before any write operation
   python3 tools/validate_repository_boundaries.py --check-path ./output/blog/new-post.md
   ```

3. **Assembly command:**
   ```
   ASSEMBLE blog theme: ai-agents length: medium
   ```

4. **Assembler behavior:**
   - Reads `config.yaml`
   - Resolves knowledge repository path (e.g., `../knowledge-base/knowledge`)
   - Reads blocks from external path
   - Validates output path is allowed
   - Writes only to `./output/blog/`

---

## Example 7: CI/CD Integration

### Scenario
Enforcing repository boundaries in CI/CD pipeline.

### GitHub Actions Example

```yaml
name: Validate Repository Boundaries

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive  # If using submodules
      
      - name: Validate boundaries
        run: |
          python3 tools/validate_repository_boundaries.py
      
      - name: Check knowledge access
        run: |
          python3 tools/validate_repository_boundaries.py --check-knowledge-access
```

---

## Validation Best Practices

### Before Assembly Operations

Always validate before writing:
```bash
python3 tools/validate_repository_boundaries.py --check-path <target-output-path>
```

### During Development

Add pre-commit hook:
```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 tools/validate_repository_boundaries.py
if [ $? -ne 0 ]; then
    echo "ERROR: Repository boundary validation failed"
    exit 1
fi
```

### Regular Audits

Run full validation:
```bash
# Check configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access

# Check all protected paths
for path in knowledge/blocks knowledge/candidates knowledge/INVARIANTS.md; do
    python3 tools/validate_repository_boundaries.py --check-path "$path"
done
```

---

## Troubleshooting Examples

### Issue: "Path is protected" error

**Problem:** Trying to write to `knowledge/blocks/`

**Solution:**
```bash
# Check what paths are protected
cat config.yaml | grep -A 10 boundaries

# Use correct output path
# Correct: ./output/blog/post.md
# Wrong: ./knowledge/blocks/new-block.md
```

### Issue: "Knowledge repository access validation failed"

**Problem:** External repo not configured as read-only

**Solution:**
```bash
# Check config.yaml
cat config.yaml | grep -A 5 knowledge

# Fix: Set read_only: true
# Then verify:
python3 tools/validate_repository_boundaries.py --check-knowledge-access
```

### Issue: Submodule not initialized

**Problem:** Knowledge repository path not found

**Solution:**
```bash
# Initialize submodules
git submodule update --init --recursive

# Or clone with submodules
git clone --recursive <repo-url>
```

---

## Related Documentation

- **Setup Guide:** `docs/Multi-Repository-Setup.md`
- **Architectures:** `knowledge/blocks/frameworks/repository-split-architectures.md`
- **Structure:** `knowledge/blocks/frameworks/private-repository-structure.md`
