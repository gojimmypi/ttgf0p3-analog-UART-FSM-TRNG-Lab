#!/bin/bash
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: run_tests.sh
#
# Windows: PORT=COM8
# Linux:   PORT=/dev/ttyUSB0
# macOS:   PORT=/dev/tty.usbserial-0001
# WSL:     PORT=/dev/ttyS8

PORT=/dev/ttyS8

# Run shell check to ensure this a good script.
# Specify the executable shell checker you want to use:
MY_SHELLCHECK="shellcheck"

# Check if the executable is available in the PATH
if command -v "$MY_SHELLCHECK" >/dev/null 2>&1; then
    # Run your command here
    shellcheck "$0" || exit 1
else
    echo "$MY_SHELLCHECK is not installed. Please install it if changes to this script have been made."
fi

# usage: tt_ulx3s_uart_test.py [-h] --port PORT [--baud BAUD] [--timeout TIMEOUT] [--idle-time IDLE_TIME]
#                              [--repeat REPEAT] [--stop-on-fail]
#                              [--reset-registers]

python tt_ulx3s_uart_test.py --port $PORT  

python tt_ulx3s_uart_test.py --port $PORT --reset-registers
