#!/bin/bash
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: ice40/run_tests.sh
#

set -e
set -o pipefail

echo "**************************************************************************"
echo "**  Begin ${BASH_SOURCE[0]} from ${PWD}"
echo "This test requires external UART TTY connected to TT RX == IN3, TX == OUT0"
echo "**************************************************************************"

# Windows: PORT=COM8
# WSL:     PORT=/dev/ttyS8
# Linux:   PORT=/dev/ttyUSB8 or /dev/ttyACM8
# macOS:   PORT=/dev/tty.usbserial-0008
#
# The TT_UART_PORT is the external USB TTY device, typically connected to IN3/Rx and OUT4/Tx.
# The TT port is the board with the REPL prompt, not the connected external UART adapter.
if [ -z "${MY_TT_UART_PORT:-}" ]; then
    MY_TT_UART_PORT=/dev/ttyS8
fi

if [ -z "${MY_TT_PORT:-}" ]; then
    MY_TT_PORT=/dev/ttyS6
fi

if [ -z "${TT_UART_PORT:-}" ]; then
    TT_UART_PORT="${MY_TT_UART_PORT}"
fi

if [ -z "${TT_PORT:-}" ]; then
    TT_PORT="${MY_TT_PORT}"
fi

export TT_UART_PORT
export TT_PORT

# WARNING: This is NOT the TT_PORT for the Tiny Tapeout Demoboard.
# This port is the external UART connected to the PMOD pins!
echo "TT_UART_PORT: ${TT_UART_PORT}"
echo "TT_PORT:      ${TT_PORT}"

# Run shellcheck to ensure this is a good script.
# Specify the executable shell checker you want to use:
MY_SHELLCHECK="shellcheck"

# Check if the executable is available in the PATH
if command -v "$MY_SHELLCHECK" >/dev/null 2>&1; then
    # Run your command here 
    "$MY_SHELLCHECK" -x "${BASH_SOURCE[0]}" || exit 1
else
    echo "$MY_SHELLCHECK is not installed. Please install it if changes to this script have been made."
fi

# Setup environment
echo "**************************************************************************"
echo "**  Setup environment"
echo "**************************************************************************"
source ./env_ice40.sh

echo "**************************************************************************"
echo "**  Calling project reset script on TT Port ${TT_PORT}"
echo "**************************************************************************"
./project_reset.sh || exit 1


echo "**************************************************************************"
echo "**  Calling test scripts on UART Port ${TT_UART_PORT}"
echo "**************************************************************************"

python ../test-hw/tt_uart_test.py --port "$TT_UART_PORT"                   || exit 1

python ../test-hw/tt_uart_test.py --port "$TT_UART_PORT" --reset-registers || exit 1

python ../test-hw/tt_trng_uart_test.py --port "$TT_UART_PORT"              || exit 1

python ../test-hw/tt_trng_repro_test.py --port  "$TT_UART_PORT"            || exit 1

python ../test-hw/tt_uart_test.py --port "$TT_UART_PORT" --reset-registers || exit 1

echo "**************************************************************************"
echo "**  Done. Ports used:"
echo "**************************************************************************"
echo "TT_UART_PORT: ${TT_UART_PORT}"
echo "TT_PORT:      ${TT_PORT}"
