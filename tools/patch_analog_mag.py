#!/usr/bin/env python3
"""Patch the generated GF180 analog frame MAG file.

The raw tt_analog_1x2.def frame provides the TT signal and analog pins.  Keep
those analog pin geometries unchanged so the exported LEF matches the Tiny
Tapeout analog template exactly.  Add only project power ports here; inward
analog connectivity stubs are added to the GDS after export so they do not
change LEF pin dimensions.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

# Magic internal units.  These rails are full-height edge ports so precheck
# does not report the project power pins as too far from the top/bottom edges.
POWER_PORTS = [
    ("VGND", 0, 0, 100, 32536, "ground", "bidirectional"),
    ("VDPWR", 34564, 0, 34664, 32536, "power", "bidirectional"),
]


def add_power_rects(text: str) -> str:
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
    text = add_power_rects(text)
    text = add_power_labels(text)
    path.write_text(text)

    required = ["ua[0]", "ua[1]", "ua[2]", "ua[3]", "ua[4]", "ua[5]", "VGND", "VDPWR"]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError("MAG patch missing: " + ", ".join(missing))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
