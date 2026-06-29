#!/usr/bin/env bash
set -euo pipefail

TOP="tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab_analog"
TT_TOOL="${TT_TOOL:-/mnt/c/workspace/tt-support-tools-gojimmypi/tt_tool.py}"
PROJECT_V="src/project.v"
PROJECT_V_BAK="build/full_harden/project.v.before_full_harden"

if [ -z "${PDK_ROOT:-}" ]; then
    echo "ERROR: PDK_ROOT is not set"
    exit 1
fi

if [ ! -x "${TT_TOOL}" ]; then
    echo "ERROR: TT_TOOL is not executable: ${TT_TOOL}"
    echo "Set TT_TOOL=/path/to/tt_tool.py if needed."
    exit 1
fi

restore_project_v() {
    if [ -f "${PROJECT_V_BAK}" ]; then
        cp -f "${PROJECT_V_BAK}" "${PROJECT_V}"
        echo "Restored ${PROJECT_V}"
    fi
}

find_hardened_file() {
    local kind="$1"
    local name="$2"
    local result

    result="$({ find runs -type f -path "*/final/${kind}/${name}" -printf '%T@ %p\n' 2>/dev/null || true; } |
        sort -n |
        tail -n 1 |
        sed 's/^[^ ]* //')"

    if [ -z "${result}" ]; then
        echo "ERROR: Could not find hardened ${kind^^} output for ${name}" >&2
        echo "Expected something like runs/.../final/${kind}/${name}" >&2
        return 1
    fi

    printf '%s\n' "${result}"
}

copy_hardened_outputs() {
    local gds_src
    local lef_src

    gds_src="$(find_hardened_file gds "${TOP}.gds")"
    lef_src="$(find_hardened_file lef "${TOP}.lef")"

    mkdir -p gds lef
    cp -f "${gds_src}" "gds/${TOP}.gds"
    cp -f "${lef_src}" "lef/${TOP}.lef"

    echo
    echo "Copied hardened outputs:"
    ls -lh "gds/${TOP}.gds" "lef/${TOP}.lef"

    python3 tools/check_gds_content.py "gds/${TOP}.gds"
}

mkdir -p "$(dirname "${PROJECT_V_BAK}")"
cp -f "${PROJECT_V}" "${PROJECT_V_BAK}"
trap restore_project_v EXIT

python3 tools/patch_full_harden_source.py "${PROJECT_V}"

"${TT_TOOL}" --gf --create-user-config
python3 tools/patch_full_harden_config.py
"${TT_TOOL}" --gf --harden --no-docker

restore_project_v
trap - EXIT

copy_hardened_outputs

echo
echo "Done. Commit the regenerated files under gds/ and lef/ after inspection."
