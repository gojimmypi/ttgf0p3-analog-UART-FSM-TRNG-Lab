#!/usr/bin/env python3
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: test-hw/capture_trng_raw_uart.py

import argparse
import sys
import time

import serial


def write_cmd(ser, cmd):
    ser.write(cmd)
    ser.flush()


def read_exact(ser, count):
    data = bytearray()

    while len(data) < count:
        chunk = ser.read(count - len(data))

        if not chunk:
            raise TimeoutError(f"timeout after {len(data)} of {count} bytes")

        data.extend(chunk)

    return bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True)
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--bytes", type=int, default=1024)
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    if args.bytes < 1:
        print("error: --bytes must be at least 1", file=sys.stderr)
        return 1

    with serial.Serial(args.port, args.baud, timeout=args.timeout) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        time.sleep(0.1)

        # Recommended raw capture setup:
        # E0: freeze while configuring
        # S3: mixed source
        # OFF: enable all oscillator bits
        # D01: fast sample divider
        # E1: enable free-running sampling
        for cmd in (b"E0\r", b"S3\r", b"OFF\r", b"D01\r", b"E1\r"):
            write_cmd(ser, cmd)
            ser.read_until(b"\r")

        remaining = args.bytes

        with open(args.out, "wb") as f:
            while remaining:
                chunk_len = min(remaining, 255)
                cmd = f"B{chunk_len:02X}\r".encode("ascii")

                write_cmd(ser, cmd)

                data = read_exact(ser, chunk_len)
                f.write(data)

                remaining -= chunk_len

    return 0


if __name__ == "__main__":
    sys.exit(main())
