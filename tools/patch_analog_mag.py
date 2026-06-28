#!/usr/bin/env python3
"""Patch the generated GF180 analog frame MAG file.

The raw tt_analog_1x2.def frame provides the TT signal and analog pins, but it
has no local inward analog stubs and no VGND/VDPWR project ports.  This patch
adds short Metal4 stubs for ua[0]..ua[5] and Metal4 power pins so the custom
analog scaffold matches Tiny Tapeout precheck expectations.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

UA_STUBS = {
    "ua[0]": (32582, 0, 32882, 3000),
    "ua[1]": (28214, 0, 28514, 3000),
    "ua[2]": (23846, 0, 24146, 3000),
    "ua[3]": (19478, 0, 19778, 3000),
    "ua[4]": (15110, 0, 15410, 3000),
    "ua[5]": (10742, 0, 11042, 3000),
}

POWER_PORTS = [
    ("VGND", 0, 2000, 100, 30536, "ground", "bidirectional"),
    ("VDPWR", 34564, 2000, 34664, 30536, "power", "bidirectional"),
]


def replace_or_add_rects(text: str) -> str:
    for _, rect in UA_STUBS.items():
        x1, y1, x2, y2 = rect
        old_re = re.compile(rf"^rect {x1} 0 {x2} 100$", re.MULTILINE)
        new_line = f"rect {x1} {y1} {x2} {y2}"
        if old_re.search(text):
            text = old_re.sub(new_line, text)
        elif new_line not in text:
            text = text.replace("<< labels >>", new_line + "\n<< labels >>", 1)

    for _, x1, y1, x2, y2, _, _ in POWER_PORTS:
        line = f"rect {x1} {y1} {x2} {y2}"
        if line not in text:
            text = text.replace("<< labels >>", line + "\n<< labels >>", 1)

    return text


def add_power_labels(text: str) -> str:
    if "flabel metal4" not in text:
        raise RuntimeError("No labels section found")

    max_port = -1
    for match in re.finditer(r"^port\s+(\d+)\s+", text, re.MULTILINE):
        max_port = max(max_port, int(match.group(1)))

    insert = []
    next_port = max_port + 1
    for name, x1, y1, x2, y2, use, direction in POWER_PORTS:
        if re.search(rf"\s{name}$", text, re.MULTILINE):
            continue
        insert.append(f"flabel metal4 s {x1} {y1} {x2} {y2} 0 FreeSans 736 90 0 0 {name}")
        insert.append(f"port {next_port} nsew {use} {direction}")
        next_port += 1

    if insert:
        marker = "<< properties >>"
        text = text.replace(marker, "\n".join(insert) + "\n" + marker, 1)

    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mag_file", help="MAG file to patch in place")
    args = parser.parse_args()

    path = Path(args.mag_file)
    text = path.read_text()
    text = replace_or_add_rects(text)
    text = add_power_labels(text)
    path.write_text(text)

    required = ["ua[0]", "ua[1]", "ua[2]", "ua[3]", "ua[4]", "ua[5]", "VGND", "VDPWR"]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError("MAG patch missing: " + ", ".join(missing))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
