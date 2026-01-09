#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual-Repository Setup Script

Sets up a dual-repository architecture where knowledge-base is external
to the main knowledge-os repository.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import yaml


def update_config(config_path: Path, knowledge_path: str, architecture: str = "dual-repo") -> None:
    """Update config.yaml with dual-repo settings"""
    config = {
        'architecture': architecture,
        'knowledge': {
            'root_path': knowledge_path,
            'integration': 'external',
            'read_only': True,
            'enforce_read_only': True
        },
        'pipeline': {
            'config_path': './knowledge/pipelines/pipeline.yaml',
            'output_dir': './output',
            'enforce_boundaries': True
        },
        'boundaries': {
            'protected_paths': [
                './knowledge/blocks',
                './knowledge/candidates',
                './knowledge/INVARIANTS.md',
                './knowledge/DECISIONS.md',
                './knowledge/MAP.md'
            ],
            'allowed_output_paths': ['./output', './drafts'],
            'validate_before_assembly': True
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Updated {config_path} with dual-repo configuration")


def setup_submodule(submodule_path: Path, repo_url: str = None) -> None:
    """Set up git submodule for knowledge repository"""
    if repo_url:
        try:
            subprocess.run(
                ['git', 'submodule', 'add', repo_url, str(submodule_path)],
                check=True,
                capture_output=True
            )
            print(f"✓ Added submodule: {submodule_path}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to add submodule: {e.stderr.decode()}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"INFO: Submodule path would be: {submodule_path}")
        print("INFO: Run manually: git submodule add <repo-url> {submodule_path}")


def main():
    ap = argparse.ArgumentParser(
        description="Set up dual-repository architecture"
    )
    ap.add_argument(
        '--knowledge-path',
        type=str,
        required=True,
        help="Path to external knowledge repository (relative or absolute)"
    )
    ap.add_argument(
        '--config',
        type=Path,
        default=Path.cwd() / "config.yaml",
        help="Path to config.yaml (default: ./config.yaml)"
    )
    ap.add_argument(
        '--submodule',
        action='store_true',
        help="Set up as git submodule instead of external path"
    )
    ap.add_argument(
        '--submodule-url',
        type=str,
        help="Git URL for submodule (required if --submodule)"
    )
    
    args = ap.parse_args()
    
    if args.submodule:
        if not args.submodule_url:
            print("ERROR: --submodule-url required when using --submodule", file=sys.stderr)
            sys.exit(1)
        
        submodule_path = Path(args.knowledge_path)
        setup_submodule(submodule_path, args.submodule_url)
        integration = "submodule"
        architecture = "submodule"
    else:
        integration = "external"
        architecture = "dual-repo"
    
    update_config(args.config, args.knowledge_path, architecture)
    
    print("\n✓ Dual-repository setup complete")
    print(f"  Knowledge repository: {args.knowledge_path}")
    print(f"  Integration: {integration}")
    print(f"  Read-only: enabled")


if __name__ == "__main__":
    main()
