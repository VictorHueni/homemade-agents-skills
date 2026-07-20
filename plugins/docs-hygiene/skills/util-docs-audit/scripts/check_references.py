#!/usr/bin/env python3
"""
Check a documentation file for broken references, dead links,
and code drift against the repository.

Outputs a JSON report of issues found.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def extract_internal_links(content: str) -> list:
    """Extract markdown internal links like [text](./path) or [text](path.md)."""
    pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    links = []
    for match in re.finditer(pattern, content):
        target = match.group(2)
        # Skip external URLs, anchors-only, and mailto
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        # Strip anchors from path
        path = target.split('#')[0] if '#' in target else target
        if path:
            links.append({
                'text': match.group(1),
                'target': target,
                'path': path,
            })
    return links


def extract_external_urls(content: str) -> list:
    """Extract external URLs from markdown content."""
    pattern = r'https?://[^\s\)\]\"\'>`]+'
    return list(set(re.findall(pattern, content)))


def extract_code_references(content: str) -> dict:
    """Extract references to code artifacts from documentation."""
    refs = {
        'file_paths': [],
        'function_names': [],
        'class_names': [],
        'env_vars': [],
        'cli_commands': [],
        'config_keys': [],
    }

    # File paths in backticks or plain text (e.g., src/foo/bar.py, ./lib/utils.ts)
    file_pattern = r'`([a-zA-Z0-9_./-]+\.[a-zA-Z]{1,10})`'
    for match in re.finditer(file_pattern, content):
        path = match.group(1)
        if '/' in path and not path.startswith('http'):
            refs['file_paths'].append(path)

    # Function/method references like `functionName()` or `module.method()`
    func_pattern = r'`([a-zA-Z_]\w*(?:\.\w+)*)\(\)`'
    for match in re.finditer(func_pattern, content):
        refs['function_names'].append(match.group(1))

    # Environment variables like $VAR, ${VAR}, or `VAR_NAME`
    env_pattern = r'(?:\$\{?([A-Z][A-Z0-9_]{2,})\}?|`([A-Z][A-Z0-9_]{2,})`)'
    for match in re.finditer(env_pattern, content):
        var = match.group(1) or match.group(2)
        if var and len(var) > 2:
            refs['env_vars'].append(var)

    # CLI commands in code blocks
    cli_pattern = r'(?:^|\n)\s*(?:\$\s+)?(\w+(?:-\w+)*)\s+(?:--[\w-]+|[a-z])'
    for match in re.finditer(cli_pattern, content):
        refs['cli_commands'].append(match.group(1))

    # Deduplicate
    for key in refs:
        refs[key] = list(set(refs[key]))

    return refs


def check_internal_links(doc_path: str, repo_root: str, links: list) -> list:
    """Check if internal links point to existing files."""
    issues = []
    doc_dir = os.path.dirname(os.path.join(repo_root, doc_path))

    for link in links:
        target_path = os.path.normpath(os.path.join(doc_dir, link['path']))
        if not os.path.exists(target_path):
            issues.append({
                'type': 'broken_internal_link',
                'severity': 'high',
                'detail': f"Link [{link['text']}]({link['target']}) points to missing file",
                'target': link['path'],
            })
    return issues


def check_code_file_refs(repo_root: str, file_paths: list) -> list:
    """Check if referenced code files exist in the repo."""
    issues = []
    for fpath in file_paths:
        full = os.path.join(repo_root, fpath)
        if not os.path.exists(full):
            # Try common alternatives
            found = False
            for alt in [fpath.lstrip('./'), 'src/' + fpath, 'lib/' + fpath]:
                if os.path.exists(os.path.join(repo_root, alt)):
                    found = True
                    break
            if not found:
                issues.append({
                    'type': 'dead_code_reference',
                    'severity': 'medium',
                    'detail': f"Referenced file `{fpath}` not found in repo",
                    'target': fpath,
                })
    return issues


def check_code_drift(repo_root: str, doc_path: str, code_refs: list) -> dict:
    """Check if referenced code files changed since the doc was last updated."""
    # Get doc's last commit date
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%aI', '--', doc_path],
            cwd=repo_root, capture_output=True, text=True, timeout=10
        )
        doc_date = result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        doc_date = None

    if not doc_date:
        return {'doc_date': None, 'drifted_files': [], 'total_drift_commits': 0}

    drifted = []
    total_commits = 0

    for ref_path in code_refs:
        full = os.path.join(repo_root, ref_path)
        # Try to find the file
        check_path = ref_path
        if not os.path.exists(full):
            for alt in [ref_path.lstrip('./'), 'src/' + ref_path, 'lib/' + ref_path]:
                if os.path.exists(os.path.join(repo_root, alt)):
                    check_path = alt
                    break
            else:
                continue

        try:
            result = subprocess.run(
                ['git', 'log', f'--since={doc_date}', '--oneline', '--', check_path],
                cwd=repo_root, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                count = len(lines)
                if count > 0:
                    total_commits += count
                    drifted.append({
                        'file': check_path,
                        'commits_since_doc_update': count,
                        'latest_change': lines[0],
                    })
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    drifted.sort(key=lambda x: x['commits_since_doc_update'], reverse=True)

    return {
        'doc_last_updated': doc_date,
        'drifted_files': drifted,
        'total_drift_commits': total_commits,
    }


def check_content_quality(content: str) -> list:
    """Check for content quality signals like TODOs, placeholders, etc."""
    issues = []

    # TODO / FIXME / HACK markers
    todo_pattern = r'(?:TODO|FIXME|HACK|XXX|TEMP)\b[:\s]*(.*?)(?:\n|$)'
    for match in re.finditer(todo_pattern, content, re.IGNORECASE):
        issues.append({
            'type': 'todo_marker',
            'severity': 'low',
            'detail': f"Contains TODO/FIXME marker: {match.group(0).strip()[:80]}",
        })

    # Placeholder text
    placeholder_patterns = [
        r'(?:coming soon|to be (documented|determined|added|written|completed))',
        r'(?:TBD|TBA|WIP|N/A|PLACEHOLDER)',
        r'(?:insert .+ here|add .+ here|fill in)',
        r'(?:lorem ipsum)',
    ]
    for pattern in placeholder_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            issues.append({
                'type': 'placeholder',
                'severity': 'medium',
                'detail': f"Contains placeholder text: \"{match.group(0).strip()[:60]}\"",
            })

    # Broken image references
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    for match in re.finditer(img_pattern, content):
        target = match.group(2)
        if not target.startswith(('http://', 'https://')):
            issues.append({
                'type': 'local_image_ref',
                'severity': 'low',
                'detail': f"Local image reference: {target} (verify it exists)",
                'target': target,
            })

    return issues


def analyze_doc(repo_root: str, doc_path: str) -> dict:
    """Run all checks on a single documentation file."""
    full_path = os.path.join(repo_root, doc_path)

    try:
        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except (OSError, IOError) as e:
        return {'error': str(e), 'path': doc_path}

    internal_links = extract_internal_links(content)
    external_urls = extract_external_urls(content)
    code_refs = extract_code_references(content)

    issues = []

    # Check internal links
    issues.extend(check_internal_links(doc_path, repo_root, internal_links))

    # Check code file references
    issues.extend(check_code_file_refs(repo_root, code_refs['file_paths']))

    # Code drift analysis
    all_code_files = code_refs['file_paths']
    drift = check_code_drift(repo_root, doc_path, all_code_files)

    # Content quality
    issues.extend(check_content_quality(content))

    # Calculate staleness score (0-10)
    score = 0.0
    if drift['total_drift_commits'] > 20:
        score += 4.0
    elif drift['total_drift_commits'] > 10:
        score += 3.0
    elif drift['total_drift_commits'] > 5:
        score += 2.0
    elif drift['total_drift_commits'] > 0:
        score += 1.0

    broken_links = sum(1 for i in issues if i['type'] == 'broken_internal_link')
    dead_refs = sum(1 for i in issues if i['type'] == 'dead_code_reference')
    score += min(broken_links * 1.5, 3.0)
    score += min(dead_refs * 1.0, 2.0)

    placeholders = sum(1 for i in issues if i['type'] == 'placeholder')
    score += min(placeholders * 0.5, 1.0)

    score = min(score, 10.0)

    return {
        'path': doc_path,
        'staleness_score': round(score, 1),
        'code_drift': drift,
        'issues': issues,
        'stats': {
            'internal_links': len(internal_links),
            'external_urls': len(external_urls),
            'code_file_refs': len(code_refs['file_paths']),
            'function_refs': len(code_refs['function_names']),
            'env_var_refs': len(code_refs['env_vars']),
        },
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: check_references.py <repo_root> <doc_path>", file=sys.stderr)
        print("       check_references.py <repo_root> --all <discovery_json>", file=sys.stderr)
        sys.exit(1)

    repo_root = sys.argv[1]

    if sys.argv[2] == '--all' and len(sys.argv) > 3:
        # Batch mode: analyze all files from discovery JSON
        with open(sys.argv[3]) as f:
            discovery = json.load(f)

        results = []
        for doc in discovery['files']:
            if doc.get('is_auto_generated'):
                continue
            result = analyze_doc(repo_root, doc['path'])
            result['days_since_update'] = doc.get('days_since_update', -1)
            results.append(result)

        # Sort by staleness score
        results.sort(key=lambda r: r.get('staleness_score', 0), reverse=True)

        print(json.dumps({
            'repo_root': repo_root,
            'scan_date': datetime.now().isoformat(),
            'total_analyzed': len(results),
            'results': results,
        }, indent=2))
    else:
        # Single file mode
        doc_path = sys.argv[2]
        result = analyze_doc(repo_root, doc_path)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
