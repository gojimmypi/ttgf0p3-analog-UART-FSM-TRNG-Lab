#!/usr/bin/env bash
set -euo pipefail

TOP="${TOP:-}"
TT_TOOL="${TT_TOOL:-tt/tt_tool.py}"
PROJECT_V="src/project.v"
PROJECT_V_BAK="build/full_harden/project.v.before_full_harden"
ARTIFACT_DIR="${ARTIFACT_DIR:-build/hardened-gds-lef}"

if [ -z "${TOP}" ]; then
    TOP="$(sed -n 's/^[[:space:]]*top_module:[[:space:]]*"?\([^"]*\)"?[[:space:]]*$/\1/p' info.yaml)"
fi

if [ -z "${TOP}" ]; then
    echo "ERROR: Could not find top_module in info.yaml" >&2
    exit 1
fi

if [ -z "${PDK_ROOT:-}" ]; then
    echo "ERROR: PDK_ROOT is not set" >&2
    exit 1
fi

if [ ! -f "${TT_TOOL}" ]; then
    echo "ERROR: TT_TOOL was not found: ${TT_TOOL}" >&2
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

    result="$({ find runs -type f -path "*/final/${kind}/${name}" -printf '%T@ %p\n' 2>/dev/null || true; } |
        sort -n |
        tail -n 1 |
        sed 's/^[^ ]* //')"

    if [ -z "${result}" ]; then
        echo "ERROR: Could not find hardened ${kind} output for ${name}" >&2
        echo "Expected something like runs/.../final/${kind}/${name}" >&2
        return 1
    fi

    printf '%s\n' "${result}"
}

copy_strip_and_stage_outputs() {
    local gds_src
    local lef_src

    gds_src="$(find_hardened_file gds "${TOP}.gds")"
    lef_src="$(find_hardened_file lef "${TOP}.lef")"

    rm -rf "${ARTIFACT_DIR}"
    mkdir -p gds lef "${ARTIFACT_DIR}/gds" "${ARTIFACT_DIR}/lef"

    cp -f "${gds_src}" "gds/${TOP}.gds"
    cp -f "${lef_src}" "lef/${TOP}.lef"

    echo
    echo "Copied hardened outputs before strip:"
    ls -lh "gds/${TOP}.gds" "lef/${TOP}.lef"
    python3 tools/check_gds_content.py "gds/${TOP}.gds"

    python3 tools/strip_unused_analog_pins.py \
        --gds "gds/${TOP}.gds" \
        --lef "lef/${TOP}.lef"

    python3 tools/check_gds_content.py "gds/${TOP}.gds"

    if grep -Eq 'PIN ua\[[67]\]' "lef/${TOP}.lef"; then
        echo "ERROR: stripped LEF still contains ua[6] or ua[7]" >&2
        exit 1
    fi

    cp -f "gds/${TOP}.gds" "${ARTIFACT_DIR}/gds/${TOP}.gds"
    cp -f "lef/${TOP}.lef" "${ARTIFACT_DIR}/lef/${TOP}.lef"

    echo
    echo "Staged stripped hardened outputs:"
    ls -lh "gds/${TOP}.gds" "lef/${TOP}.lef"
    ls -lh "${ARTIFACT_DIR}/gds/${TOP}.gds" "${ARTIFACT_DIR}/lef/${TOP}.lef"
    python3 tools/check_gds_content.py "${ARTIFACT_DIR}/gds/${TOP}.gds"
}

mkdir -p "$(dirname "${PROJECT_V_BAK}")"
cp -f "${PROJECT_V}" "${PROJECT_V_BAK}"
trap restore_project_v EXIT

python3 tools/patch_full_harden_source.py "${PROJECT_V}"

run_tt_tool --gf --create-user-config
python3 tools/patch_full_harden_config.py
run_tt_tool --gf --harden

restore_project_v
trap - EXIT

copy_strip_and_stage_outputs

echo
echo "Done. The hardened-gds-lef artifact contains stripped GDS/LEF ready for custom_gds precheck."
