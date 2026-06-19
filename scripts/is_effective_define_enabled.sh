#!/usr/bin/env bash
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: scripts/is_effective_define_enabled.sh
#
# Print 1 if a Verilog preprocessor define is enabled after preprocessing
# project_config.v, otherwise print 0.
#
# This checks the effective result after `ifdef/`ifndef logic, so it works for
# derived defines such as TRNG_HEALTH_STATUS_DEBUG_PAGE_SELECT.
#
# Examples:
#   ./is_effective_define_enabled.sh ../src/project_config.v TRNG_HEALTH_STATUS_DEBUG_PAGE_SELECT
#   ./is_effective_define_enabled.sh ../src/project_config.v DEBUG_PAGE_SELECT -DTRNG_HEALTH_STATUS
#

set -euo pipefail

CONFIG="${1:-}"
DEFINE_NAME="${2:-}"

if [[ -z "$CONFIG" || -z "$DEFINE_NAME" ]]; then
    echo "usage: $0 <project_config.v> <DEFINE_NAME> [iverilog -D options...]" >&2
    exit 2
fi

shift 2

if [[ ! -f "$CONFIG" ]]; then
    echo "error: config file not found: $CONFIG" >&2
    exit 2
fi

if [[ ! "$DEFINE_NAME" =~ ^[A-Za-z_][A-Za-z0-9_\$]*$ ]]; then
    echo "error: invalid define name: $DEFINE_NAME" >&2
    exit 2
fi

if ! command -v iverilog >/dev/null 2>&1; then
    echo "error: iverilog is required for Verilog preprocessing" >&2
    echo "install with: sudo apt install iverilog" >&2
    exit 2
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

CONFIG_DIR="$(cd "$(dirname "$CONFIG")" && pwd)"
CONFIG_FILE="$(basename "$CONFIG")"
PROBE_FILE="$TMPDIR/is_effective_define_enabled_probe.v"
OUT_FILE="$TMPDIR/preprocessed.txt"

{
    echo '`default_nettype none'
    printf '`include "%s"\n' "$CONFIG_FILE"
    echo '__EFFECTIVE_DEFINE_PROBE_BEGIN__'
    printf '`ifdef %s\n' "$DEFINE_NAME"
    printf '%s=1\n' "$DEFINE_NAME"
    printf '`else\n'
    printf '%s=0\n' "$DEFINE_NAME"
    printf '`endif\n'
    echo '__EFFECTIVE_DEFINE_PROBE_END__'
    echo '`default_nettype wire'
} > "$PROBE_FILE"

iverilog -E -g2012 -I "$CONFIG_DIR" "$@" "$PROBE_FILE" -o "$OUT_FILE"

awk -v define_name="$DEFINE_NAME" '
    /^__EFFECTIVE_DEFINE_PROBE_BEGIN__/ { show = 1; next }
    /^__EFFECTIVE_DEFINE_PROBE_END__/   { show = 0; next }

    show {
        sub(/^[[:space:]]+/, "")
        sub(/[[:space:]]+$/, "")

        if ($0 == define_name "=1") {
            print "1"
            found = 1
            exit 0
        }

        if ($0 == define_name "=0") {
            print "0"
            found = 1
            exit 0
        }
    }

    END {
        if (!found) {
            exit 1
        }
    }
' "$OUT_FILE"
