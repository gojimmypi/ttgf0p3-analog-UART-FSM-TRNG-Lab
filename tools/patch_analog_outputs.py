#!/usr/bin/env python3
"""Patch generated LEF/GDS for the GF180 analog scaffold.

Keep the LEF analog pin dimensions identical to the TT analog template. Add only
post-export items that do not belong in the template pin geometry: explicit
full-height project power ports in LEF/GDS and short inward GDS Metal4 stubs for
enabled analog pins.

This script is intentionally idempotent. It removes all known experimental
ua[5] passive plate/fringe rectangles that caused GF180 M4 spacing DRC, then
uses the existing ua[5] inward Metal4 stub as the DRC-safe passive probe
structure. That stub is connected to the ua[5] pad and provides real on-chip
metal capacitance/pickup for the charge/release/sample RTL without creating any
new same-layer Metal4 gaps.
"""
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import Iterable

# GDS coordinates are in microns. These stubs intentionally start just above
# the template ua pin rectangles so the LEF pin rectangles remain unchanged
# while the GDS has adjacent inward metal for precheck connectivity.
GDS_STUBS = [
    (325.82, 1.0, 328.82, 30.0),
    (282.14, 1.0, 285.14, 30.0),
    (238.46, 1.0, 241.46, 30.0),
    (194.78, 1.0, 197.78, 30.0),
    (151.10, 1.0, 154.10, 30.0),
    (107.42, 1.0, 110.42, 30.0),
]

# The DRC-safe passive probe is the existing ua[5] inward Metal4 stub.
UA5_PASSIVE_STUB_RECT = GDS_STUBS[5]

# Remove all known bad experimental ua[5] passive plate/fringe rectangles.
# Leaving any of these in final GDS can trigger GF180 M4.2a precheck failures.
BAD_UA5_PASSIVE_RECTS = [
    # First 7-rectangle fringe version.
    (99.92, 1.95, 101.52, 3.90),
    (101.50, 1.95, 106.85, 2.25),
    (101.50, 3.35, 106.85, 3.55),
    (106.55, 1.95, 106.85, 30.00),
    (110.40, 1.15, 130.00, 1.55),
    (110.40, 2.60, 130.00, 3.00),
    (129.60, 1.15, 130.00, 3.00),
    # Second 6-rectangle fringe version.
    (99.92, 2.00, 101.52, 3.90),
    (99.92, 2.00, 106.85, 2.40),
    (106.45, 2.00, 106.85, 30.00),
    (109.80, 1.20, 130.00, 1.60),
    (109.80, 2.80, 130.00, 3.20),
    (129.60, 1.20, 130.00, 3.20),
    # Third single-plate version. This removed the internal same-layer gap, but
    # still caused one GF180 M4.2a spacing violation against existing Metal4.
    (109.80, 1.20, 130.00, 3.20),
]

POWER_RECTS = [
    (0.0, 0.0, 1.0, 325.36),
    (345.64, 0.0, 346.64, 325.36),
]

M4_LAYER = 46
M4_DATATYPE = 0
MIN_PASSIVE_WIDTH_UM = 0.40
COORD_TOL_UM = 0.001

POWER_LEF = '''  PIN VGND
    DIRECTION INOUT ;
    USE GROUND ;
    PORT
      LAYER Metal4 ;
        RECT 0.000 0.000 1.000 325.360 ;
    END
  END VGND
  PIN VDPWR
    DIRECTION INOUT ;
    USE POWER ;
    PORT
      LAYER Metal4 ;
        RECT 345.640 0.000 346.640 325.360 ;
    END
  END VDPWR
'''


def rect_key(rect: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(round(value * 1000) for value in rect)  # type: ignore[return-value]


def bbox_key(bbox) -> tuple[int, int, int, int]:
    return rect_key(
        (
            float(bbox[0][0]),
            float(bbox[0][1]),
            float(bbox[1][0]),
            float(bbox[1][1]),
        )
    )


def validate_stub_rect(rect: tuple[float, float, float, float]) -> None:
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    if width + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
        raise RuntimeError(f"ua[5] stub is too narrow: {rect}, width={width:.3f} um")
    if height + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
        raise RuntimeError(f"ua[5] stub is too short: {rect}, height={height:.3f} um")


def remove_pin_block(text: str, pin: str) -> str:
    pattern = re.compile(
        rf"^[ \t]*PIN[ \t]+{re.escape(pin)}\n.*?^[ \t]*END[ \t]+{re.escape(pin)}\n",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", text)


def patch_lef(path: Path, top: str) -> None:
    text = path.read_text(encoding="utf-8")

    # Normalize project power pins. Do not modify the template ua[*] pin
    # rectangles; precheck compares those dimensions against tt_analog_1x2.def.
    text = remove_pin_block(text, "VGND")
    text = remove_pin_block(text, "VDPWR")

    marker = f"END {top}\n"
    if marker not in text:
        raise RuntimeError(f"Could not find LEF macro end marker {marker.strip()}")
    text = text.replace(marker, POWER_LEF + marker)

    path.write_text(text, encoding="utf-8", newline="\n")


def add_rect_once(cell, gdstk, rect: tuple[float, float, float, float]) -> bool:
    target = rect_key(rect)

    for polygon in cell.polygons:
        if polygon.layer != M4_LAYER or polygon.datatype != M4_DATATYPE:
            continue
        bbox = polygon.bounding_box()
        if bbox is None:
            continue
        if bbox_key(bbox) == target:
            return False

    x1, y1, x2, y2 = rect
    cell.add(gdstk.rectangle((x1, y1), (x2, y2), layer=M4_LAYER, datatype=M4_DATATYPE))
    return True


def remove_exact_rects(cell, rects: Iterable[tuple[float, float, float, float]]) -> int:
    targets = {rect_key(rect) for rect in rects}
    to_remove = []

    for polygon in cell.polygons:
        if polygon.layer != M4_LAYER or polygon.datatype != M4_DATATYPE:
            continue
        bbox = polygon.bounding_box()
        if bbox is None:
            continue
        if bbox_key(bbox) in targets:
            to_remove.append(polygon)

    if to_remove:
        cell.remove(*to_remove)
    return len(to_remove)


def count_exact_rects(cell, rects: Iterable[tuple[float, float, float, float]]) -> dict[tuple[float, float, float, float], int]:
    counts = {rect: 0 for rect in rects}
    target_to_rect = {rect_key(rect): rect for rect in rects}

    for polygon in cell.polygons:
        if polygon.layer != M4_LAYER or polygon.datatype != M4_DATATYPE:
            continue
        bbox = polygon.bounding_box()
        if bbox is None:
            continue
        rect = target_to_rect.get(bbox_key(bbox))
        if rect is not None:
            counts[rect] += 1

    return counts


def patch_gds(path: Path) -> None:
    import gdstk

    validate_stub_rect(UA5_PASSIVE_STUB_RECT)

    lib = gdstk.read_gds(str(path))
    top_cells = lib.top_level()
    if len(top_cells) != 1:
        raise RuntimeError("Expected exactly one top-level GDS cell")
    cell = top_cells[0]

    removed_bad = remove_exact_rects(cell, BAD_UA5_PASSIVE_RECTS)

    added = 0
    for rect in GDS_STUBS:
        if add_rect_once(cell, gdstk, rect):
            added += 1

    for rect in POWER_RECTS:
        if add_rect_once(cell, gdstk, rect):
            added += 1

    labels = {label.text for label in cell.labels}
    if "VGND" not in labels:
        cell.add(gdstk.Label("VGND", (0.5, 162.68), rotation=math.pi / 2, layer=M4_LAYER, texttype=10))
    if "VDPWR" not in labels:
        cell.add(gdstk.Label("VDPWR", (346.14, 162.68), rotation=math.pi / 2, layer=M4_LAYER, texttype=10))

    stub_counts = count_exact_rects(cell, [UA5_PASSIVE_STUB_RECT])
    if stub_counts[UA5_PASSIVE_STUB_RECT] != 1:
        raise RuntimeError(
            "DRC-safe ua[5] passive M4 stub is not present exactly once: "
            + str(stub_counts)
        )

    bad_counts = count_exact_rects(cell, BAD_UA5_PASSIVE_RECTS)
    remaining_bad = [rect for rect, count in bad_counts.items() if count]
    if remaining_bad:
        raise RuntimeError("Bad ua[5] passive M4 plate/fringe rectangles still remain: " + str(remaining_bad))

    lib.write_gds(str(path))

    print(f"Patched analog GDS: {path}")
    print(f"  removed bad ua[5] passive plate/fringe rects: {removed_bad}")
    print(f"  added required stub/power rects: {added}")
    print("  verified DRC-safe ua[5] passive M4 stub: 1")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", required=True)
    parser.add_argument("--lef", required=True, type=Path)
    parser.add_argument("--gds", required=True, type=Path)
    args = parser.parse_args()

    patch_lef(args.lef, args.top)
    patch_gds(args.gds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
