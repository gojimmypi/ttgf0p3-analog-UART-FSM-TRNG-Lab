#!/usr/bin/env bash
set -euo pipefail

TOP="tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab"
PDK="${PDK:-gf180mcuD}"
DEF_FILE="mag/tt_analog_1x2.def"

if [ -z "${PDK_ROOT:-}" ]; then
    echo "ERROR: PDK_ROOT is not set"
    exit 1
fi

MAG_RC="${PDK_ROOT}/${PDK}/libs.tech/magic/gf180mcuD.magicrc"

if [ ! -f "${MAG_RC}" ]; then
    echo "ERROR: Magic rc file not found:"
    echo "  ${MAG_RC}"
    exit 1
fi

if [ ! -f "${DEF_FILE}" ]; then
    echo "ERROR: Analog DEF file not found:"
    echo "  ${DEF_FILE}"
    exit 1
fi

mkdir -p mag

rm -f "mag/${TOP}.mag"

magic \
    -dnull \
    -noconsole \
    -rcfile "${MAG_RC}" <<EOF
load ${TOP}
def read ${DEF_FILE}
save mag/${TOP}
quit -noprompt
EOF

if grep -q 'ua\[' "mag/${TOP}.mag"; then
    echo "Created analog Magic layout:"
    ls -lh "mag/${TOP}.mag"
    grep -n 'ua\[' "mag/${TOP}.mag"
else
    echo "ERROR: Created MAG file does not contain ua pins."
    exit 1
fi
