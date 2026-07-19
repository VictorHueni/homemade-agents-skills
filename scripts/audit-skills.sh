#!/bin/bash
set -u

# Audit all skills for naming consistency, frontmatter validity, and length constraints
# Usage: ./scripts/audit-skills.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Auditing skills in $REPO_ROOT..."
echo ""

# Helper functions
error() {
  echo -e "${RED}✗ $1${NC}"
  ((ERRORS++))
}

warning() {
  echo -e "${YELLOW}⚠ $1${NC}"
  ((WARNINGS++))
}

success() {
  echo -e "${GREEN}✓ $1${NC}"
}

# Collect all skills (folders with SKILL.md)
while IFS= read -r skill_dir; do
  skill_path="$REPO_ROOT/${skill_dir#./}"
  skill_name="$(basename "$skill_dir")"

  [ ! -f "$skill_path/SKILL.md" ] && continue

  echo "─────────────────────────────────────"
  echo "Skill: $skill_name"

  # 1. Check naming consistency: folder = frontmatter name field
  frontmatter_name=$(grep "^name:" "$skill_path/SKILL.md" 2>/dev/null | sed -E 's/name: *//; s/^"//; s/"$//' | head -1)

  if [ -z "$frontmatter_name" ]; then
    error "$skill_name: missing 'name:' in frontmatter"
  elif [ "$skill_name" != "$frontmatter_name" ]; then
    error "$skill_name: folder name ≠ frontmatter name (frontmatter='$frontmatter_name')"
  else
    success "Naming: folder ↔ frontmatter match"
  fi

  # 2. Check description length (max 1024 chars)
  description=$(grep "^description:" "$skill_path/SKILL.md" 2>/dev/null | sed 's/^description: *//' | sed 's/^"//' | sed 's/"$//' | head -1)
  desc_len=${#description}

  if [ -z "$description" ]; then
    error "$skill_name: missing 'description:' field"
  elif [ "$desc_len" -gt 1024 ]; then
    error "$skill_name: description too long ($desc_len > 1024 chars)"
  else
    success "Description: $desc_len chars (limit: 1024)"
  fi

  # 3. Check YAML frontmatter validity
  if ! ruby -e "require 'yaml'; YAML.unsafe_load_file('$skill_path/SKILL.md')" 2>/dev/null; then
    error "$skill_name: invalid YAML in SKILL.md"
  else
    success "YAML: valid"
  fi

  # 4. Check required frontmatter fields
  required_fields=("name" "description" "version" "status" "last_reviewed" "user-invocable" "impact")
  missing_fields=()

  for field in "${required_fields[@]}"; do
    if ! grep -q "^$field:" "$skill_path/SKILL.md"; then
      missing_fields+=("$field")
    fi
  done

  if [ ${#missing_fields[@]} -gt 0 ]; then
    error "$skill_name: missing required fields: ${missing_fields[*]}"
  else
    success "Frontmatter: all required fields present"
  fi

  # 5. Validate status field value
  status=$(grep "^status:" "$skill_path/SKILL.md" 2>/dev/null | sed 's/^status: *//' | sed 's/ *#.*//' | head -1)
  valid_statuses=("draft" "active" "deprecated" "superseded")
  status_valid=0
  for valid_status in "${valid_statuses[@]}"; do
    if [ "$status" = "$valid_status" ]; then
      status_valid=1
      break
    fi
  done

  if [ "$status_valid" -eq 0 ] && [ -n "$status" ]; then
    warning "$skill_name: status='$status' (expected: draft|active|deprecated|superseded)"
  else
    success "Status: $status"
  fi

  # 6. Check for SKILL.md existence only (structure validation)
  if [ ! -f "$skill_path/SKILL.md" ]; then
    error "$skill_name: missing SKILL.md"
  fi

  echo ""

done < <(find ./plugins -mindepth 3 -maxdepth 3 -type d -path '*/skills/*' | sort)

echo "─────────────────────────────────────"
echo ""
echo "Summary:"
echo "  Errors:   $ERRORS"
echo "  Warnings: $WARNINGS"

if [ "$ERRORS" -eq 0 ]; then
  echo -e "${GREEN}All checks passed!${NC}"
  exit 0
else
  echo -e "${RED}$ERRORS error(s) found. Fix before proceeding.${NC}"
  exit 1
fi
