#!/usr/bin/env bash
set -euo pipefail

TOP="${TOP:-tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab_analog}"
LOG_DIR="${LOG_DIR:-build/full_harden}"
LOG_FILE="${LOG_FILE:-${LOG_DIR}/generate_analog_gds.log}"
RTL_DIAG_V="${RTL_DIAG_V:-build/analog-rtl-diagnostics/project.v}"

rotate_log() {
    local path="$1"
    if [ -f "${path}" ]; then
        cp -f "${path}" "${path}.old"
        echo "Copied existing log to ${path}.old"
    fi
}

run_diagnostic_grep() {
    local label="$1"
    local pattern="$2"
    echo "Check: ${label}"
    if ! grep -En "${pattern}" "${RTL_DIAG_V}"; then
        echo "ERROR: Missing analog RTL diagnostic: ${label}" >&2
        echo "Pattern: ${pattern}" >&2
        return 1
    fi
}

mkdir -p "${LOG_DIR}" "$(dirname "${RTL_DIAG_V}")"
rotate_log "${LOG_FILE}"

{
    echo "Generating analog GDS/LEF from latest RTL"
    echo "  TOP=${TOP}"
    echo "  TT_TOOL=${TT_TOOL:-<auto>}"
    echo "  NO_DOCKER=${NO_DOCKER:-1}"
    echo

    python3 tools/build_custom_gds_verilog.py --src src --out "${RTL_DIAG_V}"
    echo "OK: expanded Verilog written to ${RTL_DIAG_V}"

    echo
    echo "Checking analog RTL diagnostics in ${RTL_DIAG_V}"
    run_diagnostic_grep "ANALOG_ENABLED define" '^[[:space:]]*`define[[:space:]]+ANALOG_ENABLED([[:space:]]|$)'
    run_diagnostic_grep "BIG16_SPI_REG define" '^[[:space:]]*`define[[:space:]]+BIG16_SPI_REG([[:space:]]|$)'
    run_diagnostic_grep "RE analog_status UART readback" 'SPI_REG_ADDR_ANALOG_STAT(US)?[[:space:]]*:[[:space:]]*read_reg[[:space:]]*=[[:space:]]*analog_status[[:space:]]*;'
    run_diagnostic_grep "RF analog_measure UART readback" 'SPI_REG_ADDR_ANALOG_MEAS[[:space:]]*:[[:space:]]*read_reg[[:space:]]*=[[:space:]]*analog_measure[[:space:]]*;'
    run_diagnostic_grep "RE analog_status SPI readback" 'SPI_REG_ADDR_ANALOG_STAT(US)?[[:space:]]*:[[:space:]]*spi_reg_rdata[[:space:]]*=[[:space:]]*analog_status[[:space:]]*;'
    run_diagnostic_grep "RF analog_measure SPI readback" 'SPI_REG_ADDR_ANALOG_MEAS[[:space:]]*:[[:space:]]*spi_reg_rdata[[:space:]]*=[[:space:]]*analog_measure[[:space:]]*;'
    run_diagnostic_grep "analog experiment instance" 'analog_experiment_stub[[:space:]]+u_analog_experiment'
    run_diagnostic_grep "analog_status connection" '\.analog_status\(analog_status\)'
    run_diagnostic_grep "analog_measure connection" '\.analog_measure\(analog_measure\)'
    run_diagnostic_grep "ua5 measurement source" 'assign[[:space:]]+analog_measure[[:space:]]*=[[:space:]]*probe_decay_q[[:space:]]*;'

    echo
    echo "Running local full harden and analog GDS post-processing"
    ./tools/full_harden_local.sh

    echo
    echo "Generated analog outputs:"
    ls -lh "gds/${TOP}.gds" "lef/${TOP}.lef"
    python3 tools/check_gds_content.py "gds/${TOP}.gds" --require-analog-passive

    echo
    echo "Done. Next recommended command:"
    echo "  python3 tt/tt_tool.py --gf --precheck"
} 2>&1 | tee "${LOG_FILE}"
