#!/usr/bin/env python3
"""Check that a custom-GDS submission contains real layout geometry.

The GF180 analog template by itself can pass basic packaging checks while still
containing only the project boundary, Metal4 pin rectangles, and labels. That is
not a useful final design. By default this script uses only the Python standard
library and checks that the GDS has enough non-frame geometry. With
--require-analog-passive it also imports gdstk and verifies the ua[5] passive
probe patch that this project adds after hardening/export.
"""
from __future__ import annotations

import argparse
import struct
from collections import Counter
from pathlib import Path
from typing import Iterable

REC_BOUNDARY = 0x08
REC_PATH = 0x09
REC_SREF = 0x0A
REC_AREF = 0x0B
REC_TEXT = 0x0C
REC_LAYER = 0x0D
REC_DATATYPE = 0x0E
REC_TEXTTYPE = 0x16
REC_ENDEL = 0x11

# GF180 analog frame/template geometry that is not enough by itself.
# Layer 46 is Metal4. Datatype 10 is used by labels/pin text in the current
# Magic export. Layer 0 contains the top-level boundary.
FRAME_ONLY_LAYERS = {
    (0, 0),
    (46, 0),
    (46, 10),
}

MIN_REAL_POLYGONS = 100
M4_LAYER = 46
M4_DATATYPE = 0
MIN_PASSIVE_WIDTH_UM = 0.40
MIN_PASSIVE_SPACING_UM = 0.40
COORD_TOL_UM = 0.001

# Keep these synchronized with tools/patch_analog_outputs.py.
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


def _read_i2(data: bytes) -> int | None:
    if len(data) < 2:
        return None
    return struct.unpack(">h", data[:2])[0]


def summarize_gds(path: Path) -> tuple[Counter[str], Counter[tuple[int | None, int | None]]]:
    data = path.read_bytes()
    offset = 0
    current_record: int | None = None
    current_layer: int | None = None
    current_type: int | None = None

    elements: Counter[str] = Counter()
    geometry: Counter[tuple[int | None, int | None]] = Counter()

    while offset + 4 <= len(data):
        length, record_type, _data_type = struct.unpack(">HBB", data[offset : offset + 4])
        if length < 4 or offset + length > len(data):
            raise RuntimeError(f"Invalid GDS record at byte offset {offset}")

        payload = data[offset + 4 : offset + length]

        if record_type == REC_BOUNDARY:
            current_record = record_type
            current_layer = None
            current_type = None
            elements["BOUNDARY"] += 1
        elif record_type == REC_PATH:
            current_record = record_type
            current_layer = None
            current_type = None
            elements["PATH"] += 1
        elif record_type == REC_SREF:
            current_record = record_type
            elements["SREF"] += 1
        elif record_type == REC_AREF:
            current_record = record_type
            elements["AREF"] += 1
        elif record_type == REC_TEXT:
            current_record = record_type
            current_layer = None
            current_type = None
            elements["TEXT"] += 1
        elif record_type == REC_LAYER:
            current_layer = _read_i2(payload)
        elif record_type in (REC_DATATYPE, REC_TEXTTYPE):
            current_type = _read_i2(payload)
        elif record_type == REC_ENDEL:
            if current_record in (REC_BOUNDARY, REC_PATH):
                geometry[(current_layer, current_type)] += 1
            current_record = None
            current_layer = None
            current_type = None

        offset += length

    if offset != len(data):
        raise RuntimeError("Trailing partial GDS record")

    return elements, geometry


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


def check_passive_rect_design_rules(rects: list[tuple[float, float, float, float]]) -> None:
    for rect in rects:
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        if width + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
            raise RuntimeError(f"ua[5] passive M4 rect is too narrow: {rect}, width={width:.3f} um")
        if height + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
            raise RuntimeError(f"ua[5] passive M4 rect is too short: {rect}, height={height:.3f} um")

    for index, rect_a in enumerate(rects):
        for rect_b in rects[index + 1 :]:
            gap = separated_gap(rect_a, rect_b)
            if gap is not None and gap > COORD_TOL_UM and gap + COORD_TOL_UM < MIN_PASSIVE_SPACING_UM:
                raise RuntimeError(
                    "ua[5] passive M4 rect spacing is too small: "
                    f"{rect_a} to {rect_b}, gap={gap:.3f} um"
                )


def check_analog_passive(path: Path) -> None:
    try:
        import gdstk
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Missing Python package gdstk. Install with: python3 -m pip install gdstk"
        ) from exc

    check_passive_rect_design_rules(UA5_PASSIVE_CAP_RECTS)

    lib = gdstk.read_gds(str(path))
    top_cells = lib.top_level()
    if len(top_cells) != 1:
        raise RuntimeError("Expected exactly one top-level GDS cell")
    cell = top_cells[0]

    passive_counts = count_exact_rects(cell, UA5_PASSIVE_CAP_RECTS)
    missing = [rect for rect, count in passive_counts.items() if count == 0]
    duplicates = [(rect, count) for rect, count in passive_counts.items() if count > 1]

    if missing:
        raise RuntimeError("Missing DRC-first ua[5] passive M4 plate: " + str(missing))
    if duplicates:
        raise RuntimeError("Duplicate DRC-first ua[5] passive M4 plate: " + str(duplicates))

    old_counts = count_exact_rects(cell, OLD_UA5_PASSIVE_CAP_RECTS)
    remaining_old = [rect for rect, count in old_counts.items() if count]
    if remaining_old:
        raise RuntimeError("Old bad ua[5] passive M4 rectangles remain: " + str(remaining_old))

    print("OK: DRC-first ua[5] passive M4 plate is present exactly once")
    print(f"  passive M4 plate rectangles: {len(UA5_PASSIVE_CAP_RECTS)}")
    print(f"  minimum checked width/spacing: {MIN_PASSIVE_WIDTH_UM:.2f} um")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gds", type=Path, help="GDS file to inspect")
    parser.add_argument(
        "--min-real-polygons",
        type=int,
        default=MIN_REAL_POLYGONS,
        help=f"minimum non-frame polygon/path count, default {MIN_REAL_POLYGONS}",
    )
    parser.add_argument(
        "--require-analog-passive",
        action="store_true",
        help="require the DRC-first ua[5] passive Metal4 plate",
    )
    args = parser.parse_args()

    if not args.gds.is_file():
        raise FileNotFoundError(args.gds)

    elements, geometry = summarize_gds(args.gds)
    total_geometry = sum(geometry.values())
    real_geometry = sum(
        count for layer_type, count in geometry.items() if layer_type not in FRAME_ONLY_LAYERS
    )

    print(f"GDS content check: {args.gds}")
    print(f"  file size: {args.gds.stat().st_size} bytes")
    print(f"  elements: {dict(elements)}")
    print(f"  geometry total: {total_geometry}")
    print(f"  non-frame geometry: {real_geometry}")
    print("  top geometry layers:")
    for (layer, datatype), count in geometry.most_common(20):
        print(f"    layer={layer} datatype={datatype}: {count}")

    if real_geometry < args.min_real_polygons:
        print()
        print("ERROR: GDS looks like only the analog frame/pins, not the final design.")
        print("The current file has too little non-frame geometry. Regenerate the")
        print("hardened layout and copy the final GDS/LEF into gds/ and lef/.")
        return 1

    print("OK: GDS contains real non-frame layout geometry")

    if args.require_analog_passive:
        check_analog_passive(args.gds)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
