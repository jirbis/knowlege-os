#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository Initialization Script

Creates the required directory structure for Knowledge OS repositories.
Supports multiple repository types based on the architecture framework.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List


def create_directory_structure(base_path: Path, structure: List[str]) -> None:
    """Create directory structure"""
    for path_str in structure:
        path = base_path / path_str
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {path}")


def init_knowledge_os_repo(base_path: Path) -> None:
    """Initialize knowledge-os (main system) repository"""
    print(f"Initializing knowledge-os repository in {base_path}...")
    
    structure = [
        "AGENTS",
        "knowledge/pipelines",
        "knowledge/themes",
        "drafts",
        "output/blog",
        "output/book",
        "output/email",
        "output/diary",
        "tools",
        "archive/exports",
        "archive/normalized",
        "index",
    ]
    
    create_directory_structure(base_path, structure)
    
    # Create minimal files
    (base_path / "README.md").touch(exist_ok=True)
    (base_path / "AGENTS.md").touch(exist_ok=True)
    (base_path / "COMMANDS.md").touch(exist_ok=True)
    (base_path / "config.yaml").touch(exist_ok=True)
    
    print(f"✓ knowledge-os repository initialized")


def init_knowledge_base_repo(base_path: Path) -> None:
    """Initialize knowledge-base (semantic layer) repository"""
    print(f"Initializing knowledge-base repository in {base_path}...")
    
    structure = [
        "knowledge/blocks/conclusions",
        "knowledge/blocks/frameworks",
        "knowledge/blocks/checklists",
        "knowledge/blocks/narratives",
        "knowledge/blocks/metaphors",
        "knowledge/candidates/book",
        "knowledge/candidates/chapters",
        "knowledge/candidates/sections",
        "knowledge/candidates/articles",
        "knowledge/candidates/posts",
        "knowledge/themes",
        "knowledge/pipelines",
    ]
    
    create_directory_structure(base_path, structure)
    
    # Create required files
    (base_path / "knowledge/INVARIANTS.md").touch(exist_ok=True)
    (base_path / "knowledge/DECISIONS.md").touch(exist_ok=True)
    (base_path / "knowledge/MAP.md").touch(exist_ok=True)
    (base_path / "README.md").touch(exist_ok=True)
    
    print(f"✓ knowledge-base repository initialized")


def init_chat_archive_repo(base_path: Path) -> None:
    """Initialize knowledge-chat-archive (raw sources) repository"""
    print(f"Initializing knowledge-chat-archive repository in {base_path}...")
    
    structure = [
        "threads",
        "raw",
        "archive/normalized",
    ]
    
    create_directory_structure(base_path, structure)
    
    # Create index directory
    (base_path / "index").mkdir(exist_ok=True)
    
    # Create README
    readme_content = """# Knowledge Chat Archive

This repository stores raw ChatGPT and Telegram conversations.

**Rules:**
- Never commit raw chats to main knowledge-os repository
- This repository is private
- Used by ArchiveSearch agent for full-text search
- Read-only access from knowledge-os
"""
    (base_path / "README.md").write_text(readme_content, encoding='utf-8')
    
    print(f"✓ knowledge-chat-archive repository initialized")


def init_book_repo(base_path: Path, book_name: str = None) -> None:
    """Initialize book-N (final manuscript) repository"""
    if book_name:
        print(f"Initializing book repository '{book_name}' in {base_path}...")
    else:
        print(f"Initializing book repository in {base_path}...")
    
    structure = [
        "chapters",
        "outline",
        "cover",
        "publishing",
        "drafts",
    ]
    
    create_directory_structure(base_path, structure)
    
    readme_content = f"""# {book_name or 'Book'} Repository

Final manuscript and publishing materials.

**Rules:**
- Contains final deliverable texts
- Imports blocks from knowledge-base read-only
- Does not contain raw chats
- Clean, lightweight repository
"""
    (base_path / "README.md").write_text(readme_content, encoding='utf-8')
    
    print(f"✓ Book repository initialized")


def init_shared_templates_repo(base_path: Path) -> None:
    """Initialize knowledge-shared-templates repository"""
    print(f"Initializing knowledge-shared-templates repository in {base_path}...")
    
    structure = [
        "block-templates",
        "chapter-templates",
        "pipeline-templates",
        "agents-templates",
    ]
    
    create_directory_structure(base_path, structure)
    
    readme_content = """# Knowledge Shared Templates

Templates shared across books and projects.

**Contents:**
- Block templates
- Chapter templates
- Pipeline templates
- Agent templates
"""
    (base_path / "README.md").write_text(readme_content, encoding='utf-8')
    
    print(f"✓ knowledge-shared-templates repository initialized")


def main():
    ap = argparse.ArgumentParser(
        description="Initialize Knowledge OS repository structures"
    )
    ap.add_argument(
        'type',
        choices=['knowledge-os', 'knowledge-base', 'chat-archive', 'book', 'shared-templates'],
        help="Repository type to initialize"
    )
    ap.add_argument(
        'path',
        type=Path,
        nargs='?',
        default=Path.cwd(),
        help="Base path for repository (default: current directory)"
    )
    ap.add_argument(
        '--book-name',
        type=str,
        help="Book name (for book repository type)"
    )
    
    args = ap.parse_args()
    
    if not args.path.exists():
        print(f"Creating directory: {args.path}")
        args.path.mkdir(parents=True, exist_ok=True)
    
    if args.type == 'knowledge-os':
        init_knowledge_os_repo(args.path)
    elif args.type == 'knowledge-base':
        init_knowledge_base_repo(args.path)
    elif args.type == 'chat-archive':
        init_chat_archive_repo(args.path)
    elif args.type == 'book':
        init_book_repo(args.path, args.book_name)
    elif args.type == 'shared-templates':
        init_shared_templates_repo(args.path)
    
    print("\n✓ Repository initialization complete")


if __name__ == "__main__":
    main()
