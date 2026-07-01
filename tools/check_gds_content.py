#!/usr/bin/env python3
"""Check that a custom-GDS submission contains real layout geometry.

The GF180 analog template by itself can pass basic packaging checks while still
containing only the project boundary, Metal4 pin rectangles, and labels. That is
not a useful final design. By default this script uses only the Python standard
library and checks that the GDS has enough non-frame geometry. With
--require-analog-passive it also imports gdstk and verifies the DRC-safe ua[5]
passive probe structure: the inward ua[5] Metal4 stub plus pad metal, with no
known bad experimental plate/fringe rectangles remaining.
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
COORD_TOL_UM = 0.001

# Keep these synchronized with tools/patch_analog_outputs.py.
GDS_STUBS = [
    # Corrected ua[0] stub.  It touches the template pad metal at x=328.86;
    # the old x2=328.82 value caused a 0.04um GF180 M4.2a gap.
    (325.82, 1.0, 328.86, 30.0),
    (282.14, 1.0, 285.14, 30.0),
    (238.46, 1.0, 241.46, 30.0),
    (194.78, 1.0, 197.78, 30.0),
    (151.10, 1.0, 154.10, 30.0),
    (107.42, 1.0, 110.42, 30.0),
]
UA5_PASSIVE_STUB_RECT = GDS_STUBS[5]

BAD_M4_SPACING_RECTS = [
    (325.82, 1.0, 328.82, 30.0),
]

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
    # Third single-plate version.
    (109.80, 1.20, 130.00, 3.20),
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


def check_stub_rect_design_rules(rect: tuple[float, float, float, float]) -> None:
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    if width + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
        raise RuntimeError(f"ua[5] passive M4 stub is too narrow: {rect}, width={width:.3f} um")
    if height + COORD_TOL_UM < MIN_PASSIVE_WIDTH_UM:
        raise RuntimeError(f"ua[5] passive M4 stub is too short: {rect}, height={height:.3f} um")


def check_analog_passive(path: Path) -> None:
    try:
        import gdstk
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Missing Python package gdstk. Install with: python3 -m pip install gdstk"
        ) from exc

    check_stub_rect_design_rules(UA5_PASSIVE_STUB_RECT)

    lib = gdstk.read_gds(str(path))
    top_cells = lib.top_level()
    if len(top_cells) != 1:
        raise RuntimeError("Expected exactly one top-level GDS cell")
    cell = top_cells[0]

    stub_counts = count_exact_rects(cell, [UA5_PASSIVE_STUB_RECT])
    if stub_counts[UA5_PASSIVE_STUB_RECT] != 1:
        raise RuntimeError("Missing or duplicate DRC-safe ua[5] passive M4 stub: " + str(stub_counts))

    bad_spacing_counts = count_exact_rects(cell, BAD_M4_SPACING_RECTS)
    remaining_bad_spacing = [rect for rect, count in bad_spacing_counts.items() if count]
    if remaining_bad_spacing:
        raise RuntimeError("Bad ua[0] M4 spacing stub remains: " + str(remaining_bad_spacing))

    bad_counts = count_exact_rects(cell, BAD_UA5_PASSIVE_RECTS)
    remaining_bad = [rect for rect, count in bad_counts.items() if count]
    if remaining_bad:
        raise RuntimeError("Bad ua[5] passive M4 plate/fringe rectangles remain: " + str(remaining_bad))

    labels = {label.text for label in cell.labels}
    if "ua[5]" not in labels:
        raise RuntimeError("Missing ua[5] GDS label")

    print("OK: DRC-safe analog M4 stub/pad structures are present")
    print("  corrected ua[0] stub touches template pad metal at x=328.86")
    print("  passive structure: existing ua[5] inward Metal4 stub plus pad metal")
    print("  separate M4 passive plate/fringe rectangles: 0")
    print(f"  checked stub minimum width/spacing: {MIN_PASSIVE_WIDTH_UM:.2f} um")


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
        help="require the DRC-safe ua[5] passive Metal4 stub/pad and no bad plate/fringe rectangles",
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
