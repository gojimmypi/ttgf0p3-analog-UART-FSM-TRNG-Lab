#!/usr/bin/env bash
set -euo pipefail

# Regenerate the final analog GDS/LEF from the latest RTL. This replaces the
# older frame-only refresh path, which could create a misleading placeholder
# GDS that was not the full hardened design.
exec ./tools/generate_analog_gds.sh "$@"
