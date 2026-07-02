#!/usr/bin/env bash
set -euo pipefail

echo "Checking for files that should not be checked in..."

# Exact repo-relative files that are generated or local-only.
FORBIDDEN_EXACT=(
    "src/_tt_fpga_top.v"
    "src/user_config.json"
    "src/config_merged.json"
)

# Repo-relative shell patterns matched against tracked files only.
# Keep this list intentionally small to avoid blocking legitimate files.
FORBIDDEN_GLOBS=(
    "*.pyc"
    "__pycache__/*"
    "*/__pycache__/*"
    "build/*"
    "runs/*"
    "mag/*"
)

fail=0

for blocked_file in "${FORBIDDEN_EXACT[@]}"; do
    if git ls-files --error-unmatch -- "$blocked_file" >/dev/null 2>&1; then
        echo "ERROR: forbidden checked-in file: $blocked_file"
        fail=1
    fi
done

if [ "${#FORBIDDEN_GLOBS[@]}" -gt 0 ]; then
    while IFS= read -r -d '' tracked_file; do
        for blocked_pattern in "${FORBIDDEN_GLOBS[@]}"; do
            if [[ "$tracked_file" == $blocked_pattern ]]; then
                echo "ERROR: forbidden checked-in file: $tracked_file"
                echo "       matched pattern: $blocked_pattern"
                fail=1
                break
            fi
        done
    done < <(git ls-files -z)
fi

if [ "$fail" -ne 0 ]; then
    echo ""
    echo "Remove generated/local-only files from git, for example:"
    echo "  git rm --cached -- src/_tt_fpga_top.v"
    echo ""
    echo "If the file is generated locally, also add it to .gitignore."
    exit 1
fi

echo "No forbidden checked-in files found."
