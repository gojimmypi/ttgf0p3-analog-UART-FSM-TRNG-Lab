#!/usr/bin/env python3
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: test-hw/capture_trng_raw_uart.py
#
# UART capture helper for the TT TRNG binary stream.
#
# Conservative protocol assumptions for the current bitstream:
#   - ASCII commands return OK\r or ?\r.
#   - Binary stream reads use Bxx\r, where xx is a hex byte count from 01..FF.
#   - The RTL build decides whether Bxx returns raw or conditioned data.
#   - U0/U1/U2/U3 may change baud before the trailing CR is fully received,
#     so baud-change commands accept an OK prefix and then verify separately.
#

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
DEFAULT_READ_TIMEOUT_RETRIES = 3
DEFAULT_CAPTURE_RETRIES = 1
DEFAULT_CHUNK_SIZE = 255
DEFAULT_BYTES = 2097152

CMD_OK = b"OK\r"
CMD_UNKNOWN = b"?\r"


class CaptureTimeoutError(TimeoutError):
    pass


class LinkRecoveryError(RuntimeError):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="Capture TRNG bytes using the UART Bxx binary stream command."
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
        help=f"Default UART baud. Default: {DEFAULT_BAUD}",
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
        help=(
            "Switch target and host to fast baud before configuring and "
            "capturing. Disabled by default because aborted fast-baud captures "
            "can leave the target in a bad state."
        ),
    )

    parser.add_argument(
        "--conditioned",
        action="store_true",
        help=(
            "Label the capture as conditioned. No runtime stream-select command "
            "is sent; the RTL build decides what Bxx returns."
        ),
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help=(
            "Label the capture as raw. No runtime stream-select command is sent; "
            "the RTL build decides what Bxx returns."
        ),
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Serial read/write timeout in seconds. Default: {DEFAULT_TIMEOUT}",
    )

    parser.add_argument(
        "--read-timeout-retries",
        type=int,
        default=DEFAULT_READ_TIMEOUT_RETRIES,
        help=(
            "Additional empty serial reads before failing one binary chunk. "
            f"Default: {DEFAULT_READ_TIMEOUT_RETRIES}"
        ),
    )

    parser.add_argument(
        "--capture-retries",
        type=int,
        default=DEFAULT_CAPTURE_RETRIES,
        help=(
            "Retry the whole capture from byte zero after a binary read timeout. "
            "Default: 1."
        ),
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Binary stream chunk size, 1..255. Default: {DEFAULT_CHUNK_SIZE}",
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


def remove_file_quietly(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def set_serial_baud(ser, baud):
    ser.baudrate = baud
    time.sleep(0.10)
    ser.reset_input_buffer()
    ser.reset_output_buffer()


def write_cmd(ser, cmd):
    ser.write(cmd)
    ser.flush()


def read_exact_or_timeout(ser, size):
    data = b""

    while len(data) < size:
        chunk = ser.read(size - len(data))
        if not chunk:
            break
        data += chunk

    return data


def read_exact_with_retries(ser, count, timeout_retries):
    data = bytearray()
    empty_reads = 0

    while len(data) < count:
        chunk = ser.read(count - len(data))

        if not chunk:
            if empty_reads >= timeout_retries:
                raise CaptureTimeoutError(
                    f"timeout after {len(data)} of {count} bytes "
                    f"after {empty_reads + 1} read timeouts"
                )

            empty_reads += 1
            continue

        empty_reads = 0
        data.extend(chunk)

    return bytes(data)


def read_cr_response(ser):
    return ser.read_until(b"\r")


def send_ascii_cmd(ser, cmd, expected=CMD_OK):
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    write_cmd(ser, cmd)
    response = read_cr_response(ser)

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

        write_cmd(ser, cmd)
        response = read_exact_or_timeout(ser, len(expected))
        return response == expected, response

    finally:
        ser.timeout = old_timeout


def try_ascii_cmd_prefix(ser, cmd, expected_prefix, timeout=SHORT_TIMEOUT):
    old_timeout = ser.timeout

    try:
        ser.timeout = timeout
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        write_cmd(ser, cmd)
        response = read_exact_or_timeout(ser, len(expected_prefix) + 1)
        return response.startswith(expected_prefix), response

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


def send_baud_cmd(ser, baud_sel):
    cmd = f"U{baud_sel:X}\r".encode("ascii")

    # Baud-change commands are special. The target may switch baud before
    # the trailing CR is completely received by the host. Accept an OK prefix.
    ok, response = try_ascii_cmd_prefix(ser, cmd, b"OK")
    if not ok:
        raise RuntimeError(
            f"unexpected response to {cmd!r}: "
            f"expected response starting with b'OK', got {response!r}"
        )

    return response


def set_target_baud(ser, baud_sel, new_baud):
    send_baud_cmd(ser, baud_sel)
    set_serial_baud(ser, new_baud)


def verify_with_e0(ser, label):
    ok, response = try_ascii_cmd(ser, b"E0\r", CMD_OK)
    if ok:
        print(f"UART command link is OK at {label}.")
        return True

    print(f"UART command link failed at {label}: got {response!r}.")
    return False


def recover_baud_if_needed(ser, default_baud, fast_baud):
    print(f"Checking UART command link at {default_baud} baud...")

    if verify_with_e0(ser, f"{default_baud} baud"):
        return default_baud

    print(f"Trying stale fast-baud recovery at {fast_baud} baud...")
    set_serial_baud(ser, fast_baud)

    if not verify_with_e0(ser, f"{fast_baud} baud"):
        set_serial_baud(ser, default_baud)
        raise LinkRecoveryError(
            "Unable to communicate at default baud or fast baud. The target is "
            "not answering UART commands. Press reset or power-cycle the board, "
            "then rerun the script."
        )

    print("Device responded at fast baud.")
    print("Restoring target UART to default baud with U0...")

    set_target_baud(ser, 0, default_baud)

    if not verify_with_e0(ser, f"{default_baud} baud"):
        raise LinkRecoveryError(
            "U0 appeared to be accepted, but default baud did not verify. "
            "Press reset or power-cycle the board, then rerun the script."
        )

    print("Default baud restored and verified.")
    return default_baud


def configure_trng(ser):
    # Recommended capture setup:
    # E0: freeze while configuring
    # S3: mixed source
    # OFF: enable all oscillator bits
    # D01: fast sample divider
    # E1: enable free-running sampling
    print("Configuring TRNG: E0, S3, OFF, D01, E1")

    for cmd in (b"E0\r", b"S3\r", b"OFF\r", b"D01\r", b"E1\r"):
        send_ascii_cmd(ser, cmd, CMD_OK)

    print("TRNG configured.")


def set_fast_baud(ser, fast_baud):
    print(f"Switching target UART to fast baud {fast_baud}")

    if fast_baud == 921600:
        baud_sel = 3
    elif fast_baud == 460800:
        baud_sel = 2
    elif fast_baud == 230400:
        baud_sel = 1
    elif fast_baud == 115200:
        baud_sel = 0
    else:
        raise RuntimeError(f"Unsupported fast baud: {fast_baud}")

    set_target_baud(ser, baud_sel, fast_baud)

    # E0 is safe here because configure_trng() runs after baud switching and
    # ends with E1. Do not call this verification after configure_trng().
    if not verify_with_e0(ser, f"{fast_baud} baud"):
        raise RuntimeError("Fast baud command appeared to be accepted, but fast baud did not verify.")

    print("Fast baud enabled and verified.")


def restore_default_baud(ser, default_baud, fast_baud_active):
    if not fast_baud_active:
        return True

    print(f"Restoring target UART to default baud {default_baud}")

    try:
        set_target_baud(ser, 0, default_baud)
    except RuntimeError as exc:
        print(f"WARNING: target default-baud restore command failed: {exc}")
        set_serial_baud(ser, default_baud)
        return False

    if not verify_with_e0(ser, f"{default_baud} baud"):
        print("WARNING: target did not verify at default baud after restore.")
        return False

    print("Default baud restored.")
    return True


def capture_binary_stream(ser, byte_count, out_path, chunk_size, timeout_retries):
    remaining = byte_count
    total = 0
    last_report = time.monotonic()

    with open(out_path, "wb") as fout:
        while remaining > 0:
            chunk_len = min(remaining, chunk_size)
            cmd = f"B{chunk_len:02X}\r".encode("ascii")

            ser.reset_input_buffer()
            write_cmd(ser, cmd)

            data = read_exact_with_retries(ser, chunk_len, timeout_retries)

            if data == CMD_UNKNOWN:
                raise RuntimeError(
                    f"target rejected binary stream command {cmd!r} with {CMD_UNKNOWN!r}"
                )

            if data.startswith(CMD_UNKNOWN):
                raise RuntimeError(
                    f"target rejected binary stream command {cmd!r}; "
                    f"first bytes were {data[:8]!r}"
                )

            fout.write(data)
            total += len(data)
            remaining -= len(data)

            now = time.monotonic()
            if now - last_report >= 2.0:
                print(f"Captured {total} of {byte_count} bytes...")
                last_report = now

    print(f"Captured {total} bytes.")


def capture_with_retries(ser, args):
    out_tmp = f"{args.out}.tmp"
    fast_baud_active = False

    if args.conditioned:
        print("Capture mode requested: conditioned")
    elif args.raw:
        print("Capture mode requested: raw")
    else:
        print("Capture mode requested: default")

    print("Using Bxx binary stream command. Stream source is selected by the RTL build.")

    if args.fast_baud:
        set_fast_baud(ser, args.fast_baud_rate)
        fast_baud_active = True

    for attempt in range(1, args.capture_retries + 1):
        if attempt > 1:
            print(
                f"Retrying capture attempt {attempt} of {args.capture_retries}",
                file=sys.stderr,
            )

        ser.reset_input_buffer()
        ser.reset_output_buffer()
        time.sleep(0.10)

        configure_trng(ser)

        try:
            capture_binary_stream(
                ser,
                args.bytes,
                out_tmp,
                args.chunk_size,
                args.read_timeout_retries,
            )
            os.replace(out_tmp, args.out)
            return fast_baud_active

        except CaptureTimeoutError as exc:
            remove_file_quietly(out_tmp)

            if attempt >= args.capture_retries:
                raise

            print(f"WARNING: capture attempt {attempt} failed: {exc}", file=sys.stderr)
            time.sleep(1.0)

    return fast_baud_active


def cleanup_after_error(args, fast_baud_active):
    try:
        cleanup_baud = args.fast_baud_rate if fast_baud_active or args.fast_baud else args.baud

        with serial.Serial(
            port=args.port,
            baudrate=cleanup_baud,
            timeout=SHORT_TIMEOUT,
            write_timeout=SHORT_TIMEOUT,
        ) as ser:
            if fast_baud_active or args.fast_baud:
                print("Attempting best-effort fast-baud cleanup...")
                try:
                    set_target_baud(ser, 0, args.baud)
                except RuntimeError as exc:
                    print(f"WARNING: cleanup U0 failed: {exc}")
                    set_serial_baud(ser, args.baud)

                verify_with_e0(ser, f"{args.baud} baud")
            else:
                print("Attempting best-effort default-baud cleanup...")
                safe_send_ascii_cmd(ser, b"E0\r", CMD_OK)

    except Exception as cleanup_exc:
        print(f"WARNING: cleanup failed: {cleanup_exc}", file=sys.stderr)


def main():
    args = parse_args()

    if args.raw and args.conditioned:
        return die("Do not use both --raw and --conditioned.")

    if args.bytes < 1:
        return die("--bytes must be at least 1.")

    if args.read_timeout_retries < 0:
        return die("--read-timeout-retries must be at least 0.")

    if args.capture_retries < 1:
        return die("--capture-retries must be at least 1.")

    if args.chunk_size < 1 or args.chunk_size > 255:
        return die("--chunk-size must be in the range 1..255.")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        return die(f"output directory does not exist: {out_dir}")

    fast_baud_active = False

    print("Begin capture...")

    try:
        with serial.Serial(
            port=args.port,
            baudrate=args.baud,
            timeout=args.timeout,
            write_timeout=args.timeout,
        ) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            time.sleep(0.10)

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
        cleanup_after_error(args, fast_baud_active)
        return 130

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        cleanup_after_error(args, fast_baud_active)
        return 1

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
