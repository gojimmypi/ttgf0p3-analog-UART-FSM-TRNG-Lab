#!/bin/bash
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: ice40/build_and_flash.sh
#

# Windows: PORT=COM6
# WSL:     PORT=/dev/ttyS6
# Linux:   PORT=/dev/ttyUSB6 or /dev/ttyACM6
# macOS:   PORT=/dev/tty.usbserial-0006

if [ -z "${MY_TT_PORT:-}" ]; then
    MY_TT_PORT="/dev/ttyS6"
fi

echo "**************************************************************************"
echo "**  Begin ${BASH_SOURCE[0]} from ${PWD}"
echo "**************************************************************************"

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


if [ -z "${TT_PORT:-}" ]; then
    echo  "info: no TT_PORT found, setting to ${MY_TT_PORT}" >&2
    TT_PORT="${MY_TT_PORT}"
else
    echo "TT_PORT:     ${TT_PORT}"
fi

# Setup environment
echo "**************************************************************************"
echo "Setup environment"
echo "**************************************************************************"
source ./env_ice40.sh

echo "**************************************************************************"
echo "Fetch current config to config_old.ini"
echo "**************************************************************************"
mpremote connect "$TT_PORT" fs cat :config.ini > config_old.ini


echo "**************************************************************************"
echo "Write config.ini"
echo "**************************************************************************"
mpremote connect "$TT_PORT" fs cp ./config.ini :config.ini

# Build
echo "Change to parent directory:"
pushd ../  || exit 1

# tt_tool.py not working locally
#
# yes, there's an inconsistency between `tt_tool.py --harden` and `tt_fpga.py harden`
#

#echo "**************************************************************************"
#echo "Running ${TT_TOOLS}/tt_tool.py harden from $(pwd)"
#echo "**************************************************************************"
#"$TT_TOOLS"/tt_tool.py --harden || exit 1

echo "**************************************************************************"
echo "Running ${TT_TOOLS}/tt_fpga.py harden from $(pwd)"
echo "**************************************************************************"
"$TT_TOOLS"/tt_fpga.py harden || exit 1

echo "**************************************************************************"
echo "Build complete, TT_PORT = $TT_PORT - proceeding to flash..."
echo "**************************************************************************"

# Flash
"$TT_TOOLS/tt_fpga.py" configure \
    --port "$TT_PORT" \
    --upload \
    --name "$TT_TOP_NAME" \
    --set-default \
    --clockrate 25000000

echo "Completed with TT_PORT: ${TT_PORT}"

popd  || exit 1

echo "Connect to repl prompt on TT_PORT ${TT_PORT} or external TT_UART_PORT to interact."
