#!/usr/bin/env python3
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: ice40/project_reset.py
#
# Do not move this file. Referenced by TT 4337 Documentation https://app.tinytapeout.com/projects/4337

import os
import sys
import time
import serial

# Windows: PORT=COM5
# WSL:     PORT=/dev/ttyS5
# Linux:   PORT=/dev/ttyUSB5 or /dev/ttyACM5
# macOS:   PORT=/dev/tty.usbserial-0005

MY_PORT = os.environ.get("MY_PORT") or "/dev/ttyS6"

port = MY_PORT

TT_TOP_NAME = os.environ.get("TT_TOP_NAME") or ""

if not TT_TOP_NAME:
    print("ERROR: TT_TOP_NAME is not set, do you need to run `source env_ice40.sh` ?")
    sys.exit(1)

cmds = [
    "from ttboard.mode import RPMode",
    f"tt.shuttle.{TT_TOP_NAME}.enable()",
    "tt.mode = RPMode.ASIC_MANUAL_INPUTS",
    "# Set clock to 25MHz",
    "tt.clock_project_PWM(25000000)",
    "tt.reset_project(True)",
    "tt.reset_project(False)",

    # Peek at dip switch setting
    # "import time",
    # 'exec(\'for i in range(40):\\n    print("ui:", hex(int(tt.ui_in.value)), "uo:", hex(int(tt.uo_out.value)))\\n    time.sleep_ms(250)\')'


#    "tt.ui_in.value = 0x08",
#    'print("raw page:", hex(int(tt.uo_out.value)))',
#    "tt.ui_in.value = 0x09",
#    'print("health page:", hex(int(tt.uo_out.value)))'
 ]

with serial.Serial(port, 115200, timeout=0.2) as ser:
    time.sleep(0.5)
    ser.reset_input_buffer()


    # Abort any previous incomplete REPL command.
    ser.write(b"\x03\r\n")
    ser.flush()
    time.sleep(0.5)
    ser.reset_input_buffer()

    for cmd in cmds:
        if cmd.startswith("#"):
            print("\r")
            print(cmd)
            continue

        line = cmd + "\r\n"
        print("\r#-------------------------------------")
        print(f"\r# Send: {cmd}")
        print("\r#-------------------------------------")
        ser.write(line.encode("utf-8"))
        ser.flush()

        if "range(40)" in cmd:
            time.sleep(11.0)
        else:
            time.sleep(1.0)

        time.sleep(1.0)

        out = ser.read(4096)
        if out:
            print(out.decode("utf-8", errors="replace"), end="")
