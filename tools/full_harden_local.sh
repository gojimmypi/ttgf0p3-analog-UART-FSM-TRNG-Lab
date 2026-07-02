#!/usr/bin/env bash
set -euo pipefail

TOP="${TOP:-tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab_analog}"
PROJECT_V="src/project.v"
PROJECT_V_BAK="build/full_harden/project.v.before_full_harden"
HARDEN_MARKER="build/full_harden/harden_start.marker"
NO_DOCKER="${NO_DOCKER:-1}"

if [ -z "${TT_TOOL:-}" ]; then
    if [ -f "tt/tt_tool.py" ]; then
        TT_TOOL="tt/tt_tool.py"
    elif [ -f "/mnt/c/workspace/tt-support-tools-gojimmypi/tt_tool.py" ]; then
        TT_TOOL="/mnt/c/workspace/tt-support-tools-gojimmypi/tt_tool.py"
    else
        TT_TOOL="tt/tt_tool.py"
    fi
fi

if [ -z "${PDK_ROOT:-}" ]; then
    echo "ERROR: PDK_ROOT is not set"
    exit 1
fi

if [ ! -f "${TT_TOOL}" ]; then
    echo "ERROR: TT_TOOL was not found: ${TT_TOOL}"
    echo "Set TT_TOOL=/path/to/tt_tool.py if needed."
    exit 1
fi

run_tt_tool() {
    python3 "${TT_TOOL}" "$@"
}

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

    result="$({ find runs -type f -path "*/final/${kind}/${name}" -newer "${HARDEN_MARKER}" -printf '%T@ %p\n' 2>/dev/null || true; } |
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
    echo "  GDS source: ${gds_src}"
    echo "  LEF source: ${lef_src}"
    ls -lh "gds/${TOP}.gds" "lef/${TOP}.lef"

    echo
    echo "Checking copied hardened GDS before analog post-processing:"
    python3 tools/check_gds_content.py "gds/${TOP}.gds"

    python3 tools/strip_unused_analog_pins.py \
        --gds "gds/${TOP}.gds" \
        --lef "lef/${TOP}.lef"

    python3 tools/patch_analog_outputs.py \
        --top "${TOP}" \
        --lef "lef/${TOP}.lef" \
        --gds "gds/${TOP}.gds"

    echo
    echo "Checking final patched analog GDS:"
    python3 tools/check_gds_content.py "gds/${TOP}.gds" --require-analog-passive
}

mkdir -p "$(dirname "${PROJECT_V_BAK}")"
cp -f "${PROJECT_V}" "${PROJECT_V_BAK}"
trap restore_project_v EXIT

python3 tools/patch_full_harden_source.py "${PROJECT_V}"

run_tt_tool --gf --create-user-config
python3 tools/patch_full_harden_config.py

HARDEN_ARGS=(--gf --harden)
if [ "${NO_DOCKER}" != "0" ]; then
    HARDEN_ARGS+=(--no-docker)
fi

: > "${HARDEN_MARKER}"
echo "Marked harden start: ${HARDEN_MARKER}"
run_tt_tool "${HARDEN_ARGS[@]}"

restore_project_v
trap - EXIT

copy_hardened_outputs

echo
echo "Done. Regenerated files:"
echo "  gds/${TOP}.gds"
echo "  lef/${TOP}.lef"
echo "Commit those files after inspection and precheck."
