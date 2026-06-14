#!/usr/bin/env python3
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: test-hw/capture_trng_raw_uart.py

import argparse
import os
import sys
import time

import serial


DEFAULT_PORT = "/dev/ttyS12"
DEFAULT_BAUD = 115200
FAST_BAUD = 921600

DEFAULT_TIMEOUT = 1.0
SHORT_TIMEOUT = 0.25

DEFAULT_BYTES = 2097152

CMD_OK = b"OK\r"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Capture raw or conditioned TRNG bytes over UART."
    )

    parser.add_argument(
        "--port",
        default=DEFAULT_PORT,
        help=f"UART port. Default: {DEFAULT_PORT}",
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=DEFAULT_BAUD,
        help=f"Initial/default UART baud. Default: {DEFAULT_BAUD}",
    )

    parser.add_argument(
        "--fast-baud-rate",
        type=int,
        default=FAST_BAUD,
        help=f"Fast UART baud used with --fast-baud. Default: {FAST_BAUD}",
    )

    parser.add_argument(
        "--bytes",
        type=int,
        default=DEFAULT_BYTES,
        help=f"Number of bytes to capture. Default: {DEFAULT_BYTES}",
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output binary file.",
    )

    parser.add_argument(
        "--fast-baud",
        action="store_true",
        help="Switch target and host to fast baud for the capture.",
    )

    parser.add_argument(
        "--conditioned",
        action="store_true",
        help="Capture conditioned TRNG stream.",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Capture raw TRNG stream.",
    )

    parser.add_argument(
        "--no-baud-recovery",
        action="store_true",
        help="Do not try to recover if the target was left at fast baud.",
    )

    return parser.parse_args()


def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def set_serial_baud(ser, baud):
    ser.baudrate = baud
    time.sleep(0.05)
    ser.reset_input_buffer()
    ser.reset_output_buffer()


def read_exact_or_timeout(ser, size):
    data = b""

    while len(data) < size:
        chunk = ser.read(size - len(data))
        if not chunk:
            break
        data += chunk

    return data


def send_ascii_cmd(ser, cmd, expected=CMD_OK):
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ser.write(cmd)
    ser.flush()

    response = read_exact_or_timeout(ser, len(expected))

    if response != expected:
        raise RuntimeError(
            f"unexpected response to {cmd!r}: expected {expected!r}, got {response!r}"
        )

    return response


def try_ascii_cmd(ser, cmd, expected=CMD_OK, timeout=SHORT_TIMEOUT):
    old_timeout = ser.timeout

    try:
        ser.timeout = timeout
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        ser.write(cmd)
        ser.flush()

        response = read_exact_or_timeout(ser, len(expected))
        return response == expected, response

    finally:
        ser.timeout = old_timeout


def safe_send_ascii_cmd(ser, cmd, expected=CMD_OK):
    try:
        send_ascii_cmd(ser, cmd, expected)
        return True

    except RuntimeError as exc:
        print(f"WARNING: cleanup command {cmd!r} failed: {exc}")
        return False

    except serial.SerialException as exc:
        print(f"WARNING: cleanup command {cmd!r} failed: {exc}")
        return False


def verify_ascii_link(ser):
    ok, response = try_ascii_cmd(ser, b"E0\r", CMD_OK)

    if ok:
        return True, response

    ok, response = try_ascii_cmd(ser, b"V\r", None if False else CMD_OK)
    return ok, response


def recover_baud_if_needed(ser, default_baud, fast_baud):
    print(f"Checking UART command link at {default_baud} baud...")

    ok, response = try_ascii_cmd(ser, b"E0\r", CMD_OK)
    if ok:
        print("UART command link is OK at default baud.")
        return

    print(
        "Default baud did not respond cleanly. "
        f"Expected {CMD_OK!r}, got {response!r}."
    )
    print(f"Trying stale fast-baud recovery at {fast_baud} baud...")

    set_serial_baud(ser, fast_baud)

    ok, response = try_ascii_cmd(ser, b"E0\r", CMD_OK)
    if not ok:
        set_serial_baud(ser, default_baud)
        raise RuntimeError(
            "Unable to communicate at default baud or fast baud. "
            f"Fast baud response was {response!r}."
        )

    print("Device responded at fast baud.")
    print("Restoring target UART to default baud with U0...")

    ok, response = try_ascii_cmd(ser, b"U0\r", CMD_OK)
    if not ok:
        set_serial_baud(ser, default_baud)
        raise RuntimeError(
            "Device responded at fast baud, but U0 default-baud restore failed. "
            f"Expected {CMD_OK!r}, got {response!r}."
        )

    set_serial_baud(ser, default_baud)

    ok, response = try_ascii_cmd(ser, b"E0\r", CMD_OK)
    if not ok:
        raise RuntimeError(
            "U0 was accepted, but default baud did not verify afterward. "
            f"Expected {CMD_OK!r}, got {response!r}."
        )

    print("Default baud restored and verified.")


def configure_trng(ser):
    print("Disable/freezes TRNG sampling with E0")
    send_ascii_cmd(ser, b"E0\r", CMD_OK)
    print("Done!")

    print("Clear TRNG/read path with C0")
    send_ascii_cmd(ser, b"C0\r", CMD_OK)
    print("Done!")

    print("Enable TRNG sampling with E1")
    send_ascii_cmd(ser, b"E1\r", CMD_OK)
    print("Done!")


def select_capture_mode(ser, args):
    if args.raw and args.conditioned:
        raise RuntimeError("Do not use both --raw and --conditioned.")

    if args.conditioned:
        print("Select conditioned TRNG stream")
        send_ascii_cmd(ser, b"B1\r", CMD_OK)
        print("Done!")
        return

    if args.raw:
        print("Select raw TRNG stream")
        send_ascii_cmd(ser, b"B0\r", CMD_OK)
        print("Done!")
        return

    print("No stream mode specified; using device current/default stream mode.")


def set_fast_baud(ser, fast_baud):
    print(f"Switching target UART to fast baud {fast_baud}")

    if fast_baud == 921600:
        cmd = b"U3\r"
    elif fast_baud == 460800:
        cmd = b"U2\r"
    elif fast_baud == 230400:
        cmd = b"U1\r"
    elif fast_baud == 115200:
        cmd = b"U0\r"
    else:
        raise RuntimeError(f"Unsupported fast baud: {fast_baud}")

    send_ascii_cmd(ser, cmd, CMD_OK)
    set_serial_baud(ser, fast_baud)

    print("Fast baud enabled.")


def restore_default_baud(ser, default_baud, fast_baud_active):
    if not fast_baud_active:
        return True

    print(f"Restoring target UART to default baud {default_baud}")

    ok = safe_send_ascii_cmd(ser, b"U0\r", CMD_OK)

    set_serial_baud(ser, default_baud)

    if not ok:
        print("WARNING: target default-baud restore command did not verify.")
        return False

    ok, response = try_ascii_cmd(ser, b"E0\r", CMD_OK)
    if not ok:
        print(
            "WARNING: target did not verify at default baud after restore. "
            f"Expected {CMD_OK!r}, got {response!r}."
        )
        return False

    print("Default baud restored.")
    return True


def read_capture_bytes(ser, byte_count, out_file):
    remaining = byte_count
    total = 0
    last_report = time.monotonic()

    with open(out_file, "wb") as fout:
        while remaining > 0:
            chunk_size = min(4096, remaining)
            chunk = ser.read(chunk_size)

            if not chunk:
                raise RuntimeError(
                    f"timeout while reading capture data after {total} bytes"
                )

            fout.write(chunk)
            total += len(chunk)
            remaining -= len(chunk)

            now = time.monotonic()
            if now - last_report >= 2.0:
                print(f"Captured {total} of {byte_count} bytes...")
                last_report = now

    print(f"Captured {total} bytes.")


def start_binary_capture(ser, args):
    if args.conditioned:
        cmd = b"BC\r"
    elif args.raw:
        cmd = b"BR\r"
    else:
        cmd = b"B\r"

    print(f"Starting binary capture with {cmd!r}")
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(cmd)
    ser.flush()


def capture_once(ser, args):
    configure_trng(ser)
    select_capture_mode(ser, args)
    start_binary_capture(ser, args)
    read_capture_bytes(ser, args.bytes, args.out)


def capture_with_retries(ser, args):
    fast_baud_active = False

    if args.fast_baud:
        set_fast_baud(ser, args.fast_baud_rate)
        fast_baud_active = True

    capture_once(ser, args)

    return fast_baud_active


def main():
    args = parse_args()

    if args.bytes <= 0:
        return die("--bytes must be greater than zero.")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        return die(f"output directory does not exist: {out_dir}")

    fast_baud_active = False

    print("Begin capture...")

    try:
        with serial.Serial(
            port=args.port,
            baudrate=args.baud,
            timeout=DEFAULT_TIMEOUT,
            write_timeout=DEFAULT_TIMEOUT,
        ) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            if not args.no_baud_recovery:
                recover_baud_if_needed(
                    ser,
                    default_baud=args.baud,
                    fast_baud=args.fast_baud_rate,
                )

            fast_baud_active = capture_with_retries(ser, args)

            restore_default_baud(
                ser,
                default_baud=args.baud,
                fast_baud_active=fast_baud_active,
            )

    except KeyboardInterrupt:
        print()
        print("Interrupted.")
        return 130

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)

        try:
            with serial.Serial(
                port=args.port,
                baudrate=args.fast_baud_rate if args.fast_baud else args.baud,
                timeout=SHORT_TIMEOUT,
                write_timeout=SHORT_TIMEOUT,
            ) as ser:
                if fast_baud_active or args.fast_baud:
                    print("Attempting best-effort fast-baud cleanup...")
                    safe_send_ascii_cmd(ser, b"E0\r", CMD_OK)
                    safe_send_ascii_cmd(ser, b"U0\r", CMD_OK)

                    set_serial_baud(ser, args.baud)
                    safe_send_ascii_cmd(ser, b"E0\r", CMD_OK)
                else:
                    print("Attempting best-effort default-baud cleanup...")
                    safe_send_ascii_cmd(ser, b"E0\r", CMD_OK)

        except Exception as cleanup_exc:
            print(f"WARNING: cleanup failed: {cleanup_exc}", file=sys.stderr)

        return 1

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())