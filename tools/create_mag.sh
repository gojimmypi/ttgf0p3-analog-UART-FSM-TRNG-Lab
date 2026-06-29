#!/usr/bin/env bash
set -euo pipefail

TOP="tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab_analog"
PDK="${PDK:-gf180mcuD}"
DEF_FILE="mag/tt_analog_1x2.def"

if [ -z "${PDK_ROOT:-}" ]; then
    echo "ERROR: PDK_ROOT is not set"
    exit 1
fi

MAG_RC="${PDK_ROOT}/${PDK}/libs.tech/magic/gf180mcuD.magicrc"
MAG_FILE="mag/${TOP}.mag"

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

rm -f "${MAG_FILE}"

magic \
    -dnull \
    -noconsole \
    -rcfile "${MAG_RC}" <<EOF
load ${TOP}
def read ${DEF_FILE}
save mag/${TOP}
quit -noprompt
EOF

python3 tools/patch_analog_mag.py "${MAG_FILE}"

echo "Created analog Magic layout:"
ls -lh "${MAG_FILE}"

echo
echo "Analog pin labels:"
grep -n 'ua\[' "${MAG_FILE}"

echo
echo "Power labels:"
grep -n 'VGND\|VDPWR' "${MAG_FILE}"

if ! grep -q 'ua\[0\]' "${MAG_FILE}"; then
    echo "ERROR: ua[0] missing from MAG."
    exit 1
fi

if ! grep -q 'VGND' "${MAG_FILE}"; then
    echo "ERROR: VGND missing from MAG."
    exit 1
fi

if ! grep -q 'VDPWR' "${MAG_FILE}"; then
    echo "ERROR: VDPWR missing from MAG."
    exit 1
fi