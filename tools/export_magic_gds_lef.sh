#!/usr/bin/env bash
set -euo pipefail

TOP="tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab"
PDK="${PDK:-gf180mcuD}"

MAG_FILE="mag/${TOP}.mag"
GDS_FILE="gds/${TOP}.gds"
LEF_FILE="lef/${TOP}.lef"

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

if [ ! -f "${MAG_FILE}" ]; then
    echo "ERROR: Magic layout file not found:"
    echo "  ${MAG_FILE}"
    echo
    echo "This prevents exporting an empty placeholder cell."
    exit 1
fi

mkdir -p gds lef

rm -f "${GDS_FILE}" "${LEF_FILE}"

magic \
    -dnull \
    -noconsole \
    -rcfile "${MAG_RC}" <<EOF
load ${MAG_FILE}
drc check
lef write ${LEF_FILE} -pinonly
gds write ${GDS_FILE}
quit -noprompt
EOF

 python3 tools/patch_analog_outputs.py \
    --top "${TOP}" \
    --lef "${LEF_FILE}" \
    --gds "${GDS_FILE}"

echo
echo "Generated files:"
ls -lh "${MAG_FILE}"
ls -lh "${LEF_FILE}"
ls -lh "${GDS_FILE}"

echo
echo "Pin checks:"
PIN_COUNT="$(grep -E '^[[:space:]]*PIN[[:space:]]+' "${LEF_FILE}" | wc -l)"
echo "LEF PIN count: ${PIN_COUNT}"

if grep -q 'PIN ua' "${LEF_FILE}"; then
    grep -n 'PIN ua' "${LEF_FILE}"
else
    echo "ERROR: No ua pins found in LEF."
    echo "This looks like a digital TT frame, not the analog custom layout."
    exit 1
fi

if grep -q 'ua\[' "${MAG_FILE}"; then
    grep -n 'ua\[' "${MAG_FILE}"
else
    echo "ERROR: No ua pins found in MAG."
    echo "This looks like a digital TT frame, not the analog custom layout."
    exit 1
fi

for power_pin in VGND VDPWR; do
    if grep -q "PIN ${power_pin}" "${LEF_FILE}"; then
        grep -n "PIN ${power_pin}" "${LEF_FILE}"
    else
        echo "ERROR: ${power_pin} not found in LEF."
        exit 1
    fi

    if grep -q "${power_pin}" "${MAG_FILE}"; then
        grep -n "${power_pin}" "${MAG_FILE}"
    else
        echo "ERROR: ${power_pin} not found in MAG."
        exit 1
    fi
done

echo
echo "Size checks:"
wc -l "${LEF_FILE}"
du -h "${GDS_FILE}"