#!/usr/bin/env python3
"""
Discover all documentation files in a repository and gather metadata.
Outputs a JSON array of doc file records with git history info.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DOC_EXTENSIONS = {'.md', '.mdx', '.rst', '.txt', '.adoc', '.asciidoc'}

DOC_DIRECTORIES = {'docs', 'doc', 'documentation', 'wiki', '.github', 'guides', 'tutorials'}

ROOT_DOC_FILES = {
    'readme.md', 'contributing.md', 'changelog.md', 'changes.md',
    'code_of_conduct.md', 'security.md', 'license.md', 'architecture.md',
    'development.md', 'setup.md', 'install.md', 'installation.md',
    'migration.md', 'upgrading.md', 'faq.md', 'troubleshooting.md',
    'api.md', 'usage.md', 'getting-started.md', 'quickstart.md',
}

SKIP_DIRS = {
    'node_modules', '.git', 'vendor', 'dist', 'build', '__pycache__',
    '.venv', 'venv', '.tox', '.mypy_cache', '.pytest_cache',
    'target', '.next', '.nuxt', 'coverage', '.turbo',
}

AUTO_GEN_INDICATORS = {
    '_build', 'site', 'public/api', 'javadoc', 'typedoc',
    'apidoc', 'swagger-ui', 'redoc', 'doxygen',
}


def is_auto_generated(path: str) -> bool:
    """Heuristic: check if the doc path looks auto-generated."""
    lower = path.lower()
    for indicator in AUTO_GEN_INDICATORS:
        if indicator in lower:
            return True
    return False


def git_last_commit_info(repo_root: str, filepath: str) -> dict:
    """Get last commit date, author, and message for a file."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ai|||%an|||%s', '--', filepath],
            cwd=repo_root, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split('|||')
            return {
                'last_commit_date': parts[0].strip() if len(parts) > 0 else None,
                'last_commit_author': parts[1].strip() if len(parts) > 1 else None,
                'last_commit_message': parts[2].strip() if len(parts) > 2 else None,
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return {'last_commit_date': None, 'last_commit_author': None, 'last_commit_message': None}


def git_commit_count(repo_root: str, filepath: str) -> int:
    """Count total commits touching a file."""
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD', '--', filepath],
            cwd=repo_root, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return int(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass
    return 0


def days_since(date_str: str) -> int:
    """Calculate days between a git date string and now."""
    if not date_str:
        return -1
    try:
        dt = datetime.fromisoformat(date_str.replace(' ', 'T').rsplit('+', 1)[0].rsplit('-', 1)[0])
        return (datetime.now() - dt).days
    except (ValueError, IndexError):
        return -1


def discover_docs(repo_root: str, extra_skip: list = None) -> list:
    """Walk the repo and find all documentation files."""
    skip = SKIP_DIRS.copy()
    if extra_skip:
        skip.update(extra_skip)

    repo = Path(repo_root).resolve()
    docs = []

    for root, dirs, files in os.walk(repo):
        # Prune skipped directories
        dirs[:] = [d for d in dirs if d not in skip and not d.startswith('.')]

        rel_root = Path(root).relative_to(repo)

        for fname in files:
            fpath = Path(root) / fname
            rel_path = str(rel_root / fname)
            ext = fpath.suffix.lower()

            is_doc = False

            # Check if in a known doc directory
            for part in rel_root.parts:
                if part.lower() in DOC_DIRECTORIES:
                    is_doc = True
                    break

            # Check if it's a root-level doc file
            if str(rel_root) == '.' and fname.lower() in ROOT_DOC_FILES:
                is_doc = True

            # Check extension
            if ext in DOC_EXTENSIONS:
                is_doc = True

            # Skip non-doc files
            if not is_doc:
                continue

            # Skip very small files (likely placeholders)
            try:
                size = fpath.stat().st_size
            except OSError:
                continue

            # Gather git info
            git_info = git_last_commit_info(repo_root, rel_path)
            commit_count = git_commit_count(repo_root, rel_path)
            age_days = days_since(git_info['last_commit_date'])

            docs.append({
                'path': rel_path,
                'size_bytes': size,
                'extension': ext,
                'is_auto_generated': is_auto_generated(rel_path),
                'last_commit_date': git_info['last_commit_date'],
                'last_commit_author': git_info['last_commit_author'],
                'last_commit_message': git_info['last_commit_message'],
                'total_commits': commit_count,
                'days_since_update': age_days,
            })

    # Sort by days since update (most stale first), unknowns at end
    docs.sort(key=lambda d: d['days_since_update'] if d['days_since_update'] >= 0 else 99999, reverse=True)

    return docs


def main():
    if len(sys.argv) < 2:
        print("Usage: discover_docs.py <repo_root> [--skip dir1,dir2]", file=sys.stderr)
        sys.exit(1)

    repo_root = sys.argv[1]
    extra_skip = []

    if '--skip' in sys.argv:
        idx = sys.argv.index('--skip')
        if idx + 1 < len(sys.argv):
            extra_skip = sys.argv[idx + 1].split(',')

    if not os.path.isdir(repo_root):
        print(f"Error: {repo_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    docs = discover_docs(repo_root, extra_skip)

    print(json.dumps({
        'repo_root': os.path.abspath(repo_root),
        'scan_date': datetime.now().isoformat(),
        'total_files': len(docs),
        'auto_generated': sum(1 for d in docs if d['is_auto_generated']),
        'files': docs,
    }, indent=2))


if __name__ == '__main__':
    main()
