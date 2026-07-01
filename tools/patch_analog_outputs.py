#!/usr/bin/env python3
"""Patch generated LEF/GDS for the GF180 analog scaffold.

Keep the LEF analog pin dimensions identical to the TT analog template. Add only
post-export items that do not belong in the template pin geometry: explicit
full-height project power ports in LEF/GDS, short inward GDS metal stubs for
enabled analog pins, and the ua[5] passive probe structure.

This script is intentionally idempotent. It first removes known old passive
probe rectangles, then adds the current DRC-margin geometry.
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

# The first two passive probe geometry attempts could trigger GF180 Metal4 DRC
# problems. Remove both exact old versions if present so rerunning this script
# fixes stale local GDS files.
# Old attempts used a two-terminal same-layer fringe structure near VGND. That
# passed the local exact-rectangle sanity check but still left a GF180 M4.2a
# spacing violation against surrounding template metal. The safer DRC-first
# structure below is a single ua[5]-connected Metal4 plate. It still creates a
# real on-chip passive plate/probe capacitance for the charge/release/sample RTL,
# but it avoids intentional same-layer M4 gaps.
UA5_PASSIVE_CAP_RECTS = [
    (109.80, 1.20, 130.00, 3.20),
]

OLD_UA5_PASSIVE_CAP_RECTS = [
    # First 7-rectangle version.
    (99.92, 1.95, 101.52, 3.90),
    (101.50, 1.95, 106.85, 2.25),
    (101.50, 3.35, 106.85, 3.55),
    (106.55, 1.95, 106.85, 30.00),
    (110.40, 1.15, 130.00, 1.55),
    (110.40, 2.60, 130.00, 3.00),
    (129.60, 1.15, 130.00, 3.00),
    # Second 6-rectangle version that still triggered one M4.2a violation.
    (99.92, 2.00, 101.52, 3.90),
    (99.92, 2.00, 106.85, 2.40),
    (106.45, 2.00, 106.85, 30.00),
    (109.80, 1.20, 130.00, 1.60),
    (109.80, 2.80, 130.00, 3.20),
    (129.60, 1.20, 130.00, 3.20),
]


POWER_RECTS = [
    (0.0, 0.0, 1.0, 325.36),
    (345.64, 0.0, 346.64, 325.36),
]

M4_LAYER = 46
M4_DATATYPE = 0
MIN_PASSIVE_WIDTH_UM = 0.40
MIN_PASSIVE_SPACING_UM = 0.40
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


def rect_width(rect: tuple[float, float, float, float]) -> float:
    return rect[2] - rect[0]


def rect_height(rect: tuple[float, float, float, float]) -> float:
    return rect[3] - rect[1]


def separated_gap(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> float | None:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b

    x_overlap = min(ax2, bx2) - max(ax1, bx1)
    y_overlap = min(ay2, by2) - max(ay1, by1)

    if x_overlap > 0 and ay2 < by1:
        return by1 - ay2
    if x_overlap > 0 and by2 < ay1:
        return ay1 - by2
    if y_overlap > 0 and ax2 < bx1:
        return bx1 - ax2
    if y_overlap > 0 and bx2 < ax1:
        return ax1 - bx2
    return None


def validate_passive_rects(rects: Iterable[tuple[float, float, float, float]]) -> None:
    rect_list = list(rects)
    for rect in rect_list:
        width = rect_width(rect)
        height = rect_height(rect)
        if width + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
            raise RuntimeError(f"Passive M4 rect is too narrow: {rect}, width={width:.3f} um")
        if height + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
            raise RuntimeError(f"Passive M4 rect is too short: {rect}, height={height:.3f} um")

    for index, rect_a in enumerate(rect_list):
        for rect_b in rect_list[index + 1 :]:
            gap = separated_gap(rect_a, rect_b)
            if gap is not None and gap > COORD_TOL_UM and gap + COORD_TOL_UM < MIN_PASSIVE_SPACING_UM:
                raise RuntimeError(
                    "Passive M4 rect spacing is too small: "
                    f"{rect_a} to {rect_b}, gap={gap:.3f} um"
                )


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

    validate_passive_rects(UA5_PASSIVE_CAP_RECTS)

    lib = gdstk.read_gds(str(path))
    top_cells = lib.top_level()
    if len(top_cells) != 1:
        raise RuntimeError("Expected exactly one top-level GDS cell")
    cell = top_cells[0]

    removed_old = remove_exact_rects(cell, OLD_UA5_PASSIVE_CAP_RECTS)

    added = 0
    for rect in GDS_STUBS:
        if add_rect_once(cell, gdstk, rect):
            added += 1

    for rect in UA5_PASSIVE_CAP_RECTS:
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

    passive_counts = count_exact_rects(cell, UA5_PASSIVE_CAP_RECTS)
    missing = [rect for rect, count in passive_counts.items() if count != 1]
    if missing:
        raise RuntimeError("DRC-first ua[5] passive M4 plate is not present exactly once: " + str(missing))

    old_counts = count_exact_rects(cell, OLD_UA5_PASSIVE_CAP_RECTS)
    remaining_old = [rect for rect, count in old_counts.items() if count]
    if remaining_old:
        raise RuntimeError("Old bad ua[5] passive M4 rectangles still remain: " + str(remaining_old))

    lib.write_gds(str(path))

    print(f"Patched analog GDS: {path}")
    print(f"  removed old ua[5] passive rects: {removed_old}")
    print(f"  added new rects: {added}")
    print(f"  verified ua[5] passive plate rects: {len(UA5_PASSIVE_CAP_RECTS)}")


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
